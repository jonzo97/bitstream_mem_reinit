module top(
input logic clk,
input logic[31:0] raddr,
input logic[31:0] waddr,
input logic [15:0] din,
output logic [15:0] dout,
input logic reset);

memory #("~/bigmems/designs/init/16_by_1024.txt", 1, 16, 1024) mem(
	.clk(clk), 
	.raddr(raddr), 
	.waddr(waddr), 
	.din(din), 
	.dout(dout), 
	.reset(reset));


endmodule