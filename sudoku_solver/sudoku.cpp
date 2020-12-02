#include <iostream>
#include <vector>
#include <stack>


//outputting the board
void out_sudoku(const std::vector<std::vector<short>>& sudoku)
{
    for (auto i = sudoku.begin(); i != sudoku.end(); ++i)
    {
        if (std::distance(sudoku.begin(), i) % 3 == 0)
            std::cout << " - - - - - - - - - - - - - - " << std::endl;

        for (auto j = i->begin(); j != i->end(); ++j)
        {
            if (std::distance(i->begin(), j) % 3 == 0)
            {
                std::cout << " | ";
            }
            if (std::distance(i->begin(), j) == 8)
            {
                std::cout << *j << " | " << std::endl;
            }
            else
            {
                std::cout << *j << " ";
            }
        }
    }
    std::cout << " - - - - - - - - - - - - - - " << std::endl; 

}

//checks whether the new value at the position pair fullfills the sudoku rules
bool check_rules(const std::pair<short, short>& pos, const std::vector<std::vector<short>>& sudoku) 
{
    short value = sudoku[pos.second][pos.first];
    //checking rows and columns
    for (short i = 0; i < sudoku.size(); i++) 
    {
        if (sudoku[pos.second][i] == value && i != pos.first)
        {
            return false;
        }
        if (sudoku[i][pos.first] == value && i != pos.second)
        {
            return false;
        }
    }
    //checking the ''square''
    short xmin = pos.first / 3;
    short ymin = pos.second / 3;
    for (short i = ymin * 3; i < ymin * 3 + 3; i++)
        for (short j = xmin * 3; j < xmin * 3 + 3; j++)
            if (sudoku[i][j] == value && i != pos.second && j != pos.first)
            {
                return false;
            }
    return true;
}



//find the next empty entry in the board, return it's pos
//return (-1,-1) if the board is already full
std::pair<short, short> find_empty(const std::vector<std::vector<short>>& sudoku) 
{
    for (auto i = sudoku.begin(); i != sudoku.end(); ++i)
        for (auto j = i->begin(); j != i->end(); ++j)
            if (*j == 0)
            {
                //returning j,i coordinates
                return std::make_pair(std::distance(i->begin(), j), std::distance(sudoku.begin(), i));
            }
    return { -1,-1 };
}


//the backtracking algo
void solver(std::vector<std::vector<short>>& sudoku) 
{
    short value;
    //stack to avoid recursion
    std::stack<std::pair<short,short>> last_pos;
    //starting point
    std::pair<short, short> pos = { 0, 0 };
    pos = find_empty(sudoku);
    while (pos.second != -1) 
    {
        //every new value is set to 1
        sudoku[pos.second][pos.first] = 1;
        value = 1;
        while (!check_rules(pos, sudoku)) 
        {
            //if still no solution and val=9, go back in the stack, backtracking...
            if (value == 9) 
            {
                sudoku[pos.second][pos.first] = 0;
                pos = last_pos.top();
                last_pos.pop();
                //increase the old value by one, backtracking...
                value = sudoku[pos.second][pos.first] + 1;
                sudoku[pos.second][pos.first] = value;
                //special case, if the previous val was already 9, go back further
                if (value > 9) 
                {
                    sudoku[pos.second][pos.first] = 0;
                    pos = last_pos.top();
                    last_pos.pop();
                    value = sudoku[pos.second][pos.first] + 1;
                    sudoku[pos.second][pos.first] = value;
                }
            }
            //iterating through 1-9, checking for a solution
            else 
            {
                sudoku[pos.second][pos.first] += 1;
                value = sudoku[pos.second][pos.first];
            }
        }
        //adding the temporary solution to the stack and finding the next 0
        last_pos.push(pos);
        pos = find_empty(sudoku);
    }
    out_sudoku(sudoku);
}


int main(){
    std::vector<std::vector<short>> board = {
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
    //solver(board);
    out_sudoku(board);
    std::cout << "The solution is:" << std::endl;
    solver(board);
}
