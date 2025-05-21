void foo(int32_t* a, int32_t* b, int32_t* c) {
    for (int i = 0; i < 4; ++i) {
        c[i] = a[i] + b[i];
    }
}
