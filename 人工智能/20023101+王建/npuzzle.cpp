#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime>

using namespace std;

class Node {
public:
    vector<vector<int>> data;
    int level;
    int fval;

    Node(vector<vector<int>> _data, int _level, int _fval) {
        data = _data;
//        data = copy(_data);
        level = _level;
        fval = _fval;
    }

    vector<vector<int>> copy(vector<vector<int>> data) {
        vector<vector<int>> temp;
        for (int i = 0; i < data.size(); i++) {
            vector<int> t;
            for (int j = 0; j < data[i].size(); j++) {
                t.push_back(data[i][j]);
            }
            temp.push_back(t);
        }
        return temp;
    }

    vector<vector<int>> shuffle(vector<vector<int>> data, int x1, int y1, int x2, int y2) {
        if (x2 >= 0 && x2 < data.size() && y2 >= 0 && y2 < data.size()) {
            vector<vector<int>> temp_data;
            temp_data = copy(data);
            int temp = temp_data[x2][y2];
            temp_data[x2][y2] = temp_data[x1][y1];
            temp_data[x1][y1] = temp;
            return temp_data;
        } else {
            return data;
        }
    }

    vector<int> find(vector<vector<int>> data, int x) {
        vector<int> ans;
        for (int i = 0; i < data.size(); i++) {
            for (int j = 0; j < data.size(); j++) {
                if (data[i][j] == x) {
                    vector<int> ans;
                    ans.push_back(i);
                    ans.push_back(j);
                    return ans;
                }
            }
        }
    }

    vector<Node> generate_child(vector<vector<int>> data) {
        vector<int> zero_position = find(data, 0);
        int x = zero_position[0], y = zero_position[1];
        vector<vector<int>> next_step
                {{x,     y - 1},
                 {x,     y + 1},
                 {x - 1, y},
                 {x + 1, y}};
        vector<Node> children;
        for (int i = 0; i < next_step.size(); i++) {
            vector<vector<int>> child = shuffle(data, x, y, next_step[i][0], next_step[i][1]);
            if (child != data) {
                Node child_node = Node(child, level + 1, 0);
                children.push_back(child_node);
            }
        }
        return children;
    }
};


bool cmp(const Node &a, const Node &b) {
    return a.fval < b.fval;
}


// refer: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
int getInvCount(int arr[]) {
    int inv_count = 0;
    for (int i = 0; i < 9 - 1; i++)
        for (int j = i+1; j < 9; j++)
            // Value 0 is used for empty space
            if (arr[j] && arr[i] &&  arr[i] > arr[j])
                inv_count++;
    return inv_count;
}


vector<int> find_zero(vector<vector<int>> goal) {
    int s = goal.size();
    vector<int> ans;
    for(int i = 0; i < s; i++) {
        for(int j = 0;j < s; j++) {
            if(goal[i][j] == 0) {
                ans.push_back(i);
                ans.push_back(j);
                return ans;
            }
        }
    }
    return ans;
}

bool isSolvable(vector<vector<int>> start, vector<vector<int>> goal) {
    int s = start.size();
    while(1) {
        vector<int> pos = find_zero(goal);
        if(pos[0] == s-1)
            break;
        goal[pos[0]][pos[1]] = goal[pos[0]+1][pos[1]];
        goal[pos[0]+1][pos[1]] = 0;

    }
    while(1) {
        vector<int> pos = find_zero(goal);
        if(pos[1] == s-1)
            break;
        goal[pos[0]][pos[1]] = goal[pos[0]][pos[1]+1];
        goal[pos[0]][pos[1]+1] = 0;

    }
    int arr_start[s * s + 5];
    int arr_goal[s * s + 5];
    for(int i = 0; i < s; i++) {
        for(int j = 0; j < s; j++) {
            arr_start[i*s+j] = start[i][j];
            arr_goal[i*s+j] = goal[i][j];
        }
    }
    for(int i = 0; i < s*s; i++) {
        for(int j = 0; j < s*s; j++) {
            if(arr_start[i] == arr_goal[j]) {
                arr_start[i] = j;
                break;
            }
        }
    }
    int invCount = getInvCount(arr_start);
    return (invCount%2 == 0);
}

class npuzzle {
public:
    int size;
    vector<Node> next_child;
    vector<Node> visited;

    npuzzle(int _size) {
        size = _size;
    }

    vector<vector<int>> accept() {
        vector<vector<int>> puzzle;
        for (int i = 0; i < size; i++) {
            vector<int> p;
            for (int j = 0; j < size; j++) {
                int x;
                cin >> x;
                p.push_back(x);
            }
            puzzle.push_back(p);
        }
        return puzzle;
    }

    int h(Node start_node, vector<vector<int>> goal) {
        // choose one heuristic
        return h2(start_node, goal);
    }
    // Hamming Distance or Misplaced Tiles
    int h1(Node start_node, vector<vector<int>> goal) {
        int ans = 0;
        vector<vector<int>> start = start_node.data;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (start[i][j] != goal[i][j] && start[i][j] != 0)
                    ans += 1;
            }
        }
        return ans;
    }

    // Manhattan Distance/Taxicab geometry
    int h2(Node start_node, vector<vector<int>> goal) {
        int ans = 0;
        vector<vector<int>> start = start_node.data;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                int flag = 0;
                for(int ii = 0; ii < size; ii++) {
                    for(int jj = 0; jj < size; jj++) {
                        if(start[i][j] == goal[ii][jj] && start[i][j] != 0) {
                            flag = 1;
                            ans += abs(i - ii) + abs(j - jj);
                            break;
                        }
                    }
                    if(flag == 1)
                        break;
                }
            }
        }
        return ans;
    }

    int f(Node start_node, vector<vector<int>> goal) {
        return h(start_node, goal) + start_node.level;
    }

    void print(Node node) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                cout << node.data[i][j] << " ";
            }
            cout << endl;
        }
    }

    void process() {
        vector<vector<int>> start = accept();
        vector<vector<int>> goal = accept();

        if(isSolvable(start, goal) == false) {
            cout << "无解" <<endl;
            return;
        }

        Node start_node = Node(start, 0, 0);
        start_node.fval = f(start_node, goal);

        next_child.push_back(start_node);

        int cnt = 0;
        while (1) {
            cout << "step: " << cnt << endl;
            cnt++;
            Node current_node = next_child[0];
            print(current_node);
            if (h(current_node, goal) == 0)
                break;
            vector<Node> next_node = current_node.generate_child(current_node.data);
            for (int i = 0; i < next_node.size(); i++) {
                next_node[i].fval = f(next_node[i], goal);
                next_child.push_back(next_node[i]);
            }
            visited.push_back(current_node);
            vector<Node>::iterator k = next_child.begin();
            next_child.erase(k);

            sort(next_child.begin(), next_child.end(), cmp);
        }
    }
};

int main() {
    clock_t start, finish;
    start = clock();

    // note: make sure the input file is exit
    const string filePath = "../npuzzle-in.txt";
    std::freopen(filePath.c_str(), "rb", stdin);
    freopen("../npuzzle-out.txt", "w", stdout);

    int n;
    cin >> n;
    npuzzle np = npuzzle(n);
    np.process();

    fclose(stdin);
    finish = clock();

    printf("\nusr time: %f s \n", double(finish - start) / CLOCKS_PER_SEC);
    return 0;
}
