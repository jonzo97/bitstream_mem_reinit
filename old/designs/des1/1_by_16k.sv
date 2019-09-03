module top(
input logic clk,
input logic[31:0] raddr,
input logic din,
input logic dout,
input logic reset);

memory #("1_by_16k.txt", "hex", 1, 16384) memNone (
	.clk(clk), 
	.raddr(raddr), 
	.waddr(waddr), 
	.din(din), 
	.dout(doutNone), 
	.reset(reset));

endmodule