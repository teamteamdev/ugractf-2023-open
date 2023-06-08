int RAND_bytes(unsigned char *buf, int num) {
    int i;
    for (i = 0; i < num; ++i) {
        buf[i] = '\0';
    }
}
