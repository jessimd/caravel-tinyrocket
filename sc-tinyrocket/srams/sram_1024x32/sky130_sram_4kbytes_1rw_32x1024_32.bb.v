// OpenRAM SRAM model
// Words: 1024
// Word size: 32

module sky130_sram_4kbytes_1rw_32x1024_32(
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
  input [10:0]  addr0;
  input           spare_wen0; // spare mask
  input [32:0]  din0;
  output [32:0] dout0;

endmodule
