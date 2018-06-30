# RPI3-RF
Radio frequency receiver and emitter tests 433 Mhz

## TODO

1. Try to show received signal live on the terminal, on the same line https://stackoverflow.com/questions/517127/how-do-i-write-output-in-same-place-on-the-console
2. Optimize that to only process when a 1 is received, and just let the 0's unprocessed
3. Reimplement the Tx to use addresses and data/commands, this seems to be more accurate than the current Tx, might require to adjust the bauds and maybe use the lightpi library https://www.instructables.com/id/Decoding-and-sending-433MHz-RF-codes-with-Arduino-/
