module on_ANC 
#(parameter dat_len = 16, 
parameter coeff_len = 32, 
parameter tap_len = 32, 
parameter mu = 16'sd4096, 
parameter noise_scle = 16'sd16384) 
(clk, rst, noise_in, desired_in, cleaned_out);

input clk;
input rst;
input signed [dat_len-1:0] noise_in; 
input signed [dat_len-1:0] desired_in;    
output reg signed [dat_len-1:0] cleaned_out; 

reg signed [coeff_len-1:0] coeff [0:tap_len-1];
reg signed [dat_len-1:0] delay_line [0:tap_len-1];

integer i;
reg signed [coeff_len+dat_len+6:0] y_acc;
reg signed [dat_len-1:0] y_out;
reg signed [dat_len-1:0] error_reg;
reg signed [95:0] prod;

wire signed [dat_len-1:0] scaled_noise;
assign scaled_noise = (y_out * noise_scle) >>> 15;

always @(posedge clk or posedge rst) begin
    if (rst) begin
        for (i = 0; i < tap_len; i = i + 1) begin
            coeff[i] <= 0;
            delay_line[i] <= 0;
        end
        cleaned_out <= 0;
    end else begin
        for (i = tap_len-1; i > 0; i = i - 1)
            delay_line[i] <= delay_line[i-1];
        delay_line[0] <= noise_in;

        y_acc = 0;
        for (i = 0; i < tap_len; i = i + 1)
            y_acc = y_acc + $signed(coeff[i]) * $signed(delay_line[i]);

        y_out = y_acc >>> 12;
        error_reg = desired_in - y_out;

        cleaned_out <= desired_in - scaled_noise;

        for (i = 0; i < tap_len; i = i + 1) begin
            prod = $signed(mu) * $signed(error_reg) * $signed(delay_line[i]);
            prod = prod >>> 15;
            coeff[i] <= coeff[i] + prod[coeff_len-1:0];
        end
    end
end

endmodule


module on_ANC_tb();

parameter dat_len = 16;
parameter tap_len = 32;
parameter mem_chuncks   = 1000000;
parameter delay_ref  = 16;

reg clk;
reg rst;
reg signed [dat_len-1:0] noise_in;
reg signed [dat_len-1:0] desired_in;
wire signed [dat_len-1:0] cleaned_out;

reg signed [dat_len-1:0] ref_mem   [0:mem_chuncks-1];
reg signed [dat_len-1:0] noisy_mem [0:mem_chuncks-1];
reg signed [dat_len-1:0] out_mem   [0:mem_chuncks-1];

integer i;

on_ANC #(dat_len,32,tap_len,16'sd4096,16'sd16384) mm (clk, rst, noise_in, desired_in, cleaned_out);

initial clk = 0;
always #5 clk = ~clk;

initial begin
    $readmemh("./Mem Files/noise ref/1/1_1.mem", ref_mem);
    $readmemh("./Mem Files/noisy sig/1/1_1.mem", noisy_mem);

    rst = 1;
    noise_in = 0;
    desired_in = 0;
    #20;
    rst = 0;

    for (i = 0; i < mem_chuncks; i = i + 1) begin
        if (i < delay_ref)
            noise_in = 0;
        else
            noise_in = ref_mem[i - delay_ref];

        desired_in = noisy_mem[i];
        #10;
        out_mem[i] = cleaned_out;
    end

    $writememh("./Mem Files/out file/1.mem", out_mem);
    $finish;
end

endmodule