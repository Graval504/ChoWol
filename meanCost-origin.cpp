// written by Firo_SF (https://github.com/FiroSF)
// this code was converted to python by using chat gpt.
#include <vector>
#include <string>
#include <iomanip>
#include <iostream>

using namespace std;

#define all(a) a.begin(), a.end()
#define F first
#define S second
#define INF 1234567890
#define MOD 1000000007
#define ll long long
#define pii pair<int, int>
#define piii pair<int, pii>

/*
.: 빈칸
b: 주사위 복제 - 이 칸에 멈춰있을 수 없음, 이전 움직임에 영향을 받음
m: 주사위 +4 - 이 칸에 멈춰있을 수 없음
y: 주사위 한번더 - 이 칸에 멈춰있을 수 없음
r: 다음 주사위 3배 - 시작할때 계산하기, 이게 dfs시 유지됨 (한턴 풀로 유지, 복제에는 따로 곱하지 않음)
w: 이후 주사위 +1 - 즉시 발동시켜야함
*/

vector<double> probv = {0, .4, .3, .2, .1};
vector<vector<vector<double>>> dp;
int N;
string s;

void dfs(int turn, int idx, int p1cnt, int last, bool istriple, double prob) {
    idx = min(N - 1, idx);

    if (s[idx] == 'b') {
        dfs(turn, idx + last, p1cnt, last, istriple, prob);

    } else if (s[idx] == 'm') {
        int mov = 4 * (istriple * 2 + 1);
        dfs(turn, idx + mov, p1cnt, mov, istriple, prob);

    } else if (s[idx] == 'y') {
        for (int i = 1; i < 5; i++) {
            int mov = (i + p1cnt) * (istriple * 2 + 1);
            dfs(turn, idx + mov, p1cnt, mov, istriple, prob * probv[i]);
        }

    } else if (s[idx] == 'r') {
        if (last != 0) {
            dp[turn][idx][p1cnt] += prob;
            return;
        }

        for (int i = 1; i < 5; i++) {
            int mov = (i + p1cnt) * 3;
            dfs(turn, idx + mov, p1cnt, mov, true, prob * probv[i]);
        }

    } else if (s[idx] == 'w') {
        if (last != 0) {
            dp[turn][idx][p1cnt + 1] += prob;
            return;
        }

        for (int i = 1; i < 5; i++) {
            int mov = i + p1cnt;
            dfs(turn, idx + mov, p1cnt, mov, false, prob * probv[i]);
        }
    } else {
        // cout << turn << " " << idx << endl;
        if (last != 0) {
            dp[turn][idx][p1cnt] += prob;
            return;
        }

        for (int i = 1; i < 5; i++) {
            int mov = i + p1cnt;
            dfs(turn, idx + mov, p1cnt, mov, false, prob * probv[i]);
        }
    }
}

int main() {
    // Fast IO
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int KMAX = 10;

    cin >> s;
    N = s.size();

    dp = vector<vector<vector<double>>>(N + 1, vector<vector<double>>(N, vector<double>(KMAX)));  // dp[i][j][k] = i턴에 j번째칸에  k(이후주사위횟수) 일 확률
    dp[0][0][0] = 1;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N - 1; j++) {
            for (int k = 0; k < KMAX; k++) {
                if (dp[i][j][k] == 0)
                    continue;

                dfs(i + 1, j, k, 0, false, dp[i][j][k]);
            }
        }
    }

    for (int i = 0; i < N; i++) {
        double probsum = 0;
        for (int k = 0; k < KMAX; k++) {
            probsum += dp[i][N - 1][k];
        }

        cout << probsum << endl;
    }

    return 0;
}

/* stuff you should look for
 * int overflow, array bounds
 * special cases (n=1?)
 * do smth instead of nothing and stay organized
 * WRITE STUFF DOWN
 * DON'T GET STUCK ON ONE APPROACH
 */