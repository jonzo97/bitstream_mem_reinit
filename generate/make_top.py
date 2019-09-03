TOPNAME = 'top.sv'
F_INIT = 'init.txt'
INIT_FRMT = "hex"
WID_MEM = 16
DEPTH_MEM = 2048
COUNT = None


def main():
    import sys
    fname = sys.argv[1]
    width = sys.argv[2]
    depth = sys.argv[3]
    f_init = sys.argv[4]
    init_frmt = "hex"  # sys.argv[5]

    if type(width) is str:
        width = int(width)
    if type(depth) is str:
        depth = int(depth)

    write_topfile(fname=fname, wid_mem=width, depth_mem=depth,
                  f_init=f_init, init_frmt=init_frmt)


def write_topfile(fname, wid_mem, f_init, depth_mem, init_frmt):
    with open(fname, 'w+') as f:
        write_top_hdr(f=f, wid_mem=wid_mem)
        write_module(f=f, f_init=f_init, init_frmt=init_frmt,
                     wid_mem=wid_mem, depth_mem=depth_mem)
        write_end(f)


def write_top_hdr(f, wid_mem=WID_MEM, dout_count=COUNT):
    module = f'module top(\n'
    module += f'input logic clk,\n'
    module += f'input logic[31:0] raddr,\n'
    module += f'input logic[31:0] waddr,\n'
    module += f'input logic [{wid_mem-1}:0] din,\n'
    if dout_count is not None:
        for x in range(dout_count):
            module += f'output logic [{wid_mem-1}:0] dout{x},\n'
    else:
        module += f'output logic [{wid_mem-1}:0] dout,\n'
    module += f'input logic reset);\n\n'
    f.write(module)


def write_module(f, f_init=F_INIT, init_frmt=INIT_FRMT, wid_mem=WID_MEM, depth_mem=DEPTH_MEM, suffix=None):
    if init_frmt == "hex":
        init_frmt = 1
    else:
        init_frmt = 0

    wires = f''
    modline = f'memory #('
    modline += f'"{f_init}", {init_frmt}, {wid_mem}, {depth_mem}) '
    if suffix is not None:
        modline += f'mem{suffix} (\n'
    else:
        modline += f'mem(\n'

    modline += f'\t.clk(clk), \n\t.raddr(raddr), \n\t.waddr(waddr), \n\t.din(din), '
    if suffix is not None:
        modline += f'\n\t.dout(dout{suffix}), '
    else:
        modline += f'\n\t.dout(dout), '
    modline += f'\n\t.reset(reset));\n\n'
    f.write(modline)


def write_end(f):
    f.write('endmodule')
    memsv = f'''
 
module memory #(
    parameter F_INIT="init.txt",
    parameter INIT_ISHEX = 1,
    //parameter WID_MEM=16,
    //parameter DEPTH_MEM=2048)
    parameter WID_MEM=1,
    parameter DEPTH_MEM=16384)    
    (input logic clk,
    input logic[31:0] raddr,
    input logic[31:0] waddr,
    input logic[WID_MEM-1:0] din,
    output logic[WID_MEM-1:0] dout,
    input logic reset);

    (* ram_style = "block" *) logic [WID_MEM-1:0] ram [0:DEPTH_MEM-1];
    
    if (INIT_ISHEX)
        initial $readmemh(F_INIT, ram);
        //initial $readmemh ("../init/1_by_16k.txt",ram);
    else
        initial $readmemb(F_INIT,ram);
    
    always_ff @(posedge clk) begin
        dout <= ram[raddr];
        ram[waddr]<= din; 
    end
endmodule
    '''
    f.write(memsv)


if __name__ == "__main__":
    main()
