// Simple UART module for I/O
module uart (
    input wire clk,
    input wire rst,
    input wire rdy,

    // CPU interface
    input  wire [31:0] addr,
    input  wire [7:0]  data_in,
    output reg  [7:0]  data_out,
    input  wire        wr,
    output reg         tx_busy,
    output reg         rx_ready
);

    // Simple UART simulation model
    always @(posedge clk) begin
        if (rst) begin
            tx_busy <= 1'b0;
            rx_ready <= 1'b0;
            data_out <= 8'h0;
        end else if (rdy) begin
            if (wr && addr == 32'h30000) begin
                // Write to UART
                $write("%c", data_in);
                tx_busy <= 1'b0;
            end
            if (addr == 32'h30004) begin
                // Status register
                data_out <= 8'h0;  // Not busy
            end
        end
    end

endmodule
