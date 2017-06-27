BIN_matmul = matmul
OBJS_matmul = main.o matmul2d.o \
matmul2d_jk_novec.o matmul2d_kj_novec.o \
matmul2d_kj_vec_k.o matmul2d_kj_vec_j.o matmul2d_kj_vec_kj.o \
matmul2d_jk_vec_k.o matmul2d_jk_vec_j.o matmul2d_jk_vec_jk.o

CFLAGS = -Wall -g -O2 -fopenmp -D N=1024
ASFLAGS = -m64 -D N=1024

all: $(OBJS_matmul)
		gcc $(CFLAGS) -o $(BIN_matmul) $^

.c.o:
		gcc $(CFLAGS) -c -o $@ $<
.S.o:
		gcc $(ASFLAGS) -c -o $@ $<

clean:
		rm -f $(BIN_matmul) $(OBJS_matmul)