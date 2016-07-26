#!/usr/bin/env python
# Copyright (c) 2016 PLUMgrid
# Licensed under the Apache License, Version 2.0 (the "License")

import bcc
import multiprocessing
import time
import unittest

class TestPerfCounter(unittest.TestCase):
    def test_cycles(self):
        text = """
BPF_PERF_ARRAY(cycles, NUM_CPUS);
BPF_HISTOGRAM(dist);
int kprobe__sys_nanosleep(void *ctx) {
    u64 key = cycles.perf_read(bpf_get_smp_processor_id());
    dist.increment(bpf_log2l(key));
    return 0;
}
"""
        b = bcc.BPF(text=text, debug=0,
                cflags=["-DNUM_CPUS=%d" % multiprocessing.cpu_count()])
        b["cycles"].open_perf_event(3, 2<<0|0<<8|0<<16)
        time.sleep(0.1)
        b["dist"].print_log2_hist()

if __name__ == "__main__":
    unittest.main()
