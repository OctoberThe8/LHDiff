#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <sys/types.h>
#include <sys/wait.h>

#define GOAL 50

void run_player(const char *name, int read_fd, int write_fd) 
{
    int total = 0;
    int token;
    int roll;

    srand(time(NULL) ^ getpid());

    for (;;) 
	{
        /* Wait for referee to give us the turn */
        if (read(read_fd, &token, sizeof(token)) <= 0)
		 {
            _exit(0);

        }

        printf("%s: rolling the dice...\n", name);
        roll = (rand() % 10) + 1;      /* 1–10 */
        total += roll;

        printf("%s: rolled %d, total = %d\n\n", name, roll, total);

        /* Send current total back to the referee */
        if (write(write_fd, &total, sizeof(total)) < 0) 
		{
            _exit(1);
        }
    }
}

int main(void)  
{
    int p1_ref[2 ], ref_p1[2];
    int p2_ref[2] , ref_p2[2];
    pid_t pid1, pid2;
    int token=1;
    int score1 = 0, score2 = 0 ;

    printf("Referee: starting a two-player dice game.\n");
    printf("First player to reach %d points wins.\n\n", GOAL);

    if (pipe(p1_ref) == -1 || pipe(ref_p1) == -1 ||pipe(p2_ref) == -1 || pipe(ref_p2) == -1) 
	{
        perror("pipe");
        return 1;
    }

    pid1 = fork();
    if (pid1 == 0) 
	{
        /* Player A process */
        close(p1_ref[1]);
        close(ref_p1[0]);
        close(p2_ref[0]); close(p2_ref[1]);
        close(ref_p2[0]); close(ref_p2[1]);
        run_player("Player A", p1_ref[0], ref_p1[1]);
        _exit(0);
    }

    pid2 = fork();
    if (pid2 == 0) 
	{
        /* Player B process */
        close(p2_ref[1]);
        close(ref_p2[0]);
        close(p1_ref[0]); close(p1_ref[1]);
        close(ref_p1[0]); close(ref_p1[1]);
        run_player("Player B", p2_ref[0], ref_p2[1]);
        _exit(0);
    }

    /* Referee process */
    close(p1_ref[0]); close(ref_p1[1]);
    close(p2_ref[0]); close(ref_p2[1]);

    for (;;) {
        /* Turn for Player A */
        printf("Referee: it's Player A's turn.\n");
        if (write(p1_ref[1], &token, sizeof(token)) < 0) break;
        if (read(ref_p1[0], &score1, sizeof(score1)) <= 0) break;

        if (score1 >= GOAL) {
            printf("Referee: Player A wins with %d points!\n", score1);
            kill(pid1, SIGTERM);
            kill(pid2, SIGTERM);
            break;
        }

        /* Turn for Player B */
        printf("Referee: it's Player B's turn.\n");
        if (write(p2_ref[1], &token, sizeof(token)) < 0) break;
        if (read(ref_p2[0], &score2, sizeof(score2)) <= 0) break;

        if (score2 >= GOAL) {
            printf("Referee: Player B wins with %d points!\n", score2);
            kill(pid1, SIGTERM);
            kill(pid2, SIGTERM);
            break;
        }
    }

    close(p1_ref[1]); close(ref_p1[0]);
    close(p2_ref[1]); close(ref_p2[0]);

    wait(NULL);
    wait(NULL);

    return 0;
}
