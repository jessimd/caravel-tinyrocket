module sky130_sram_5kbytes_1rw_37x1024_37(
// `ifdef USE_POWER_PINS
    // inout vccd1,
    // inout vssd1,
// `endif
    // Port 0: RW
        clk0,csb0,web0,spare_wen0,addr0,din0,dout0,vccd1,vssd1
      );
  input  clk0; // clock
  input   csb0; // active low chip select
  input  web0; // active low write control
  input [9:0]  addr0;
  input           spare_wen0; // spare mask
  input [36:0]  din0;
  output [36:0] dout0;
  inout vccd1;
    inout vssd1;

  endmodule
  