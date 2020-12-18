#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void display (char *line, char *temp, char *filename);
int main() {
	char line[100];
	char temp[100];
	char filename[1000];
	strcpy(line, "hi i am Gaurav My name is Gaurav\n");
	strcpy(temp, "name");
	strcpy(filename, "sahil");
	display (line, temp, filename);
	return 0;
}
void display (char *line, char *temp, char *filename) {
	int number[10];
	int k = 0, i = 0;
	while (line[i] != '\0') {
		if ((line[i] == temp[0] || line[i] == temp[0] + 32 || line[i] == temp[0] - 32) && line[i] != '\0') {
			int j = 0;
			while ((line[i + j] == temp[j] || line[i + j] == temp[j] + 32 || line[i + j] == temp[j] - 32) && temp[j] != '\0') {
				j++;
			}
			if (j == strlen(temp)) {
				 number[k] = i;
				 k++;
			}
		}
		i++;
	}
	i = 0;
	//printf(" k = %d\n", k);
	/*while (k) {
		printf("%d\n", number[k - 1]);
		k--;
	}*/
	while (line[i] != '\0') {
		int dup_k = k;
		while (k) {
			int y = number[dup_k - k];
			while (i < (y)) {
				printf("%c", line[i]);
				i++;
			}
			int strc = strlen(temp);
			printf("\033[1;31m");
			while (strc) {
				int kite = 1;
				printf("%c", line[i]);
				i++;
				strc--;
			}
			printf("\033[0m");
			printf(" ");
			k--;
		}
		i++;
		printf("%c", line[i]);
	}
}
