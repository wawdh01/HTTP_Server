#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
int main() {
	int fd;
	fd = open ("Queue/queue.c", O_RDONLY);
	if (fd == -1) {
		printf("Unable to open file \n");
	}
	else {
		printf("successfull\n");
	}
	return 0;
}

