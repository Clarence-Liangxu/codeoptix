// test_vaddq_s8.c
void foo(int8_t* a, int8_t* b, int8_t* c) {
    for (int i = 0; i < 16; ++i) {
        c[i] = a[i] + b[i];
    }
}
