# ANC_nlms

An adaptive noise cancellation (ANC) system implemented in Verilog using an LMS-based FIR filter. The design supports real-time coefficient updates and includes a full testbench workflow using external memory files.

---

## Overview

This project demonstrates hardware-based adaptive filtering for removing noise from signals. It uses the Least Mean Squares (LMS) algorithm to dynamically adjust coefficients based on input and error feedback. The implementation is synthesizable and simulation-ready.

---

## Core Features

### Adaptive FIR Filter
- 32-tap FIR structure (configurable)
- LMS coefficient update:  
  $\( w_i(n+1) = w_i(n) + \mu \cdot e(n) \cdot x_i(n) \)$
- Real-time adaptation per clock

### Noise Cancellation Output
- Error computation:  
  $\( e(n) = \text{desired} - \text{filter output} \)$
- Estimated noise is scaled and subtracted from the desired signal

### Parameterized Design
Configurable through Verilog parameters:
- `dat_len` (data width)
- `coeff_len` (coefficient width)
- `tap_len` (number of taps)
- `mu` (learning rate)
- `noise_scle` (output scaling)

---

## Testbench (on_ANC_tb)

The testbench simulates a real adaptive noise cancellation environment.

### Signal Loading
Loads `.mem` files using `$readmemh()`:
- `ref_mem` → reference noise
- `noisy_mem` → noisy desired signal

### Clock and Reset
- Clock toggles every 5ns
- Reset initializes delay line and coefficients

### Processing Loop
- Adds delay to the noise reference
- Streams inputs into the DUT
- Collects cleaned output into `out_mem`

### Output Storage
Writes filtered output to:
./Mem Files/out file/1.mem

---

## Directory Structure
├── on_ANC.v         &emsp;  # Main ANC module <br>
├── on_ANC_tb.v      &nbsp; # Testbench <br>
├── Mem Files/ <br>
&emsp;  ├── noise ref/ <br>
&emsp;  ├── noisy sig/ <br>
&emsp;  └── out file/ <br>

---

## Applications

- Active noise control in communication systems  
- Real-time audio noise suppression  
- Biomedical signal cleaning (ECG, EEG)  
- FPGA/ASIC-based adaptive filtering  
