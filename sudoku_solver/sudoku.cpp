#include <iostream>
#include <vector>
#include <stack>
using namespace std;

//outputting the board
void out_sudoku(vector<vector<int>> sudoku){
    for(int i = 0; i < sudoku.size(); i++){
        if(i%3 == 0)
            cout << " - - - - - - - - - - - - - - " << endl;
        for(int j=0; j < sudoku[0].size(); j++){
            if(j % 3 == 0)
                cout << " | ";
            if(j == 8)
                cout << sudoku[i][j] << " | " << endl;
            else
                cout << sudoku[i][j] << " ";
        }
    }
    cout << " - - - - - - - - - - - - - - " << endl;
}

//checking if the value at pos fulfills the sudoku rules
bool check_rules(vector<int> pos, vector<vector<int>> sudoku){
    int value = sudoku[pos[1]][pos[0]];
    //checking rows and columns
    for(int i = 0; i < sudoku.size(); i++){
            if(sudoku[pos[1]][i] == value && i != pos[0])
                return false;
            if(sudoku[i][pos[0]] == value && i != pos[1])
                return false;
    }
    //checking the ''square''
    int xmin = pos[0] / 3;
    int ymin = pos[1] / 3;
    for(int i = ymin * 3; i < ymin * 3 + 3; i++)
        for(int j = xmin * 3; j < xmin * 3 + 3; j++)
            if(sudoku[i][j] == value && i != pos[1] && j != pos[0])
                return false;
    return true;
}

//find the next empty entry in the board, return it's pos
//return (-1,-1) if the board is already full
vector<int> find_empty(int y, vector<vector<int>> sudoku){
    for(int i = 0; i < sudoku.size(); i++)
        for(int j=0; j < sudoku[0].size(); j++)
            if(sudoku[j][i] == 0)
                return {i,j};
    return {-1,-1};
}

//the backtracking algo
void solver(vector<vector<int>> sudoku){
    int value;
    //stack to avoid recursion
    stack<vector<int>> last_pos;
    //starting point
    vector<int> pos = {0, 0};
    pos = find_empty(pos[1], sudoku);
    while(pos[0] != -1){
        //every new value is set to 1
        sudoku[pos[1]][pos[0]] = 1;
        value = 1;
        while(!check_rules(pos, sudoku)){
            //if still no solution and val=9, go back in the stack, backtracking...
            if(value == 9){
                sudoku[pos[1]][pos[0]] = 0;
                pos = last_pos.top();
                last_pos.pop();
                //increase the old value by one, backtracking...
                value = sudoku[pos[1]][pos[0]] + 1;
                sudoku[pos[1]][pos[0]] = value;
                //special case, if the previous val was already 9, go back further
                if(value > 9){
                    sudoku[pos[1]][pos[0]] = 0;
                    pos = last_pos.top();
                    last_pos.pop();
                    value = sudoku[pos[1]][pos[0]] + 1;
                    sudoku[pos[1]][pos[0]] = value;
                }
            }
            //iterating through 1-9, checking for a solution
            else{
                sudoku[pos[1]][pos[0]] += 1;
                value = sudoku[pos[1]][pos[0]];
            }
        }
        //adding the temporary solution to the stack and finding the next 0
        last_pos.push(pos);
        pos = find_empty(pos[1],sudoku);
    }
    out_sudoku(sudoku);
}

int main(){
    vector<vector<int>> board = {
        {0,0,0,0,0,0,0,0,1},
        {0,0,0,0,1,0,2,3,0},
        {0,0,8,4,3,0,0,0,7},
        {0,9,6,0,2,7,0,4,8},
        {0,0,0,0,0,9,0,0,0},
        {0,5,0,0,0,0,0,0,0},
        {0,0,4,0,0,5,0,0,0},
        {0,0,0,0,9,0,1,0,0},
        {9,8,2,7,0,0,0,0,0}

    };
    solver(board);
}
