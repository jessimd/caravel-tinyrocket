// OpenRAM SRAM model
// Words: 64
// Word size: 21

module sky130_sram_0kbytes_1rw_21x64_21(
`ifdef USE_POWER_PINS
    vccd1,
    vssd1,
`endif
// Port 0: RW
    clk0,csb0,web0,spare_wen0,addr0,din0,dout0
  );

`ifdef USE_POWER_PINS
    inout vccd1;
    inout vssd1;
`endif
  input  clk0; // clock
  input   csb0; // active low chip select
  input  web0; // active low write control
  input [6:0]  addr0;
  input           spare_wen0; // spare mask
  input [21:0]  din0;
  output [21:0] dout0;

endmodule
