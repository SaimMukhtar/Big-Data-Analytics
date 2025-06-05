#include <iostream>
#include <iomanip>
#include <cstring>
#include <limits>
#include<string>
#include <cstdlib>
#include <climits>

using namespace std;

// Struct to hold grid information
struct LList
{

    int data;
    LList* next;


    LList(int value)
    {
        data = value;
        next = NULL;
    }



};
//queue class for the linkedlist
class queue {
public:
    LList* back = NULL;
    LList* front = NULL;
    bool isempty() {
        return front == NULL;
    }
    void En_queue(int value)
    {
        LList* New_Node = new LList(value);

        if (isempty())
        {
            front = New_Node;
            back = New_Node;

        }
        else {
            back->next = New_Node;
            back = New_Node;
        }
    }
    int De_queue()
    {
        int v = 0;
        if (isempty())
        {
            cout << "Queue is empty" << endl;
        }
        else {

            LList* temporary = front;

            v = temporary->data;
            delete temporary;
        }
        return v;
    }

    bool Is_Empty() const
    {
        return front == nullptr;
    }

};
struct Grid_of_the_City
{
    int n;
    int** Grid;  // Grid representation
    int** Adj_Nodes;  // Adjacency lists

    Grid_of_the_City()
    {
        n = 0;
        Grid = nullptr;
        Adj_Nodes = nullptr;
    }

    // Get grid size from user
    void Set_Size_of_Grid()
    {
        Grid = new int* [n];
        for (int i = 0; i < n; i++)
        {
            Grid[i] = new int[n];
            if (Grid[i] == nullptr)
            {
                cout << "Error:" << endl;
                cout << "failure in Memory allocation for the grid." << endl;
                return;
            }
        }

        // Allocate memory for adjacency list
        Adj_Nodes = new int* [n * n];
        for (int i = 0; i < n * n; i++)
        {
            Adj_Nodes[i] = new int[4];  // Max 4 connections per node
            if (Adj_Nodes[i] == nullptr)
            {
                cout << "Error:" << endl;
                cout << "failure in Memory allocation for the adjacency list." << endl;
                return;
            }
            for (int j = 0; j < 4; j++)
            {
                Adj_Nodes[i][j] = -1;  // Initialize with -1 indicating no connection
            }
        }

        // Initialize grid from 1-N^2
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                Grid[i][j] = i * n + j + 1;//assigning values sequentially from 1 to 25
            }
        }

        //allocating memory for adjacency list
        //adjacency list: pointer array, each cell pointing to the a node in the grid connected to all of its neighbors in a linkedlist
        for (int i = 0; i < n * n; i++)
        {
            Adj_Nodes[i] = new int[4];  //coz max 4 connections are possible
            if (Adj_Nodes[i] == nullptr)
            {
                cout << "Error:" << endl;
                cout << "failure in Memory allocation for the adjacency list." << endl;
                return;
            }
            for (int j = 0; j < 4; j++)
            {
                Adj_Nodes[i][j] = -1;  // Initialize with -1 indicating no connection
            }
        }

        // Initialize adjacency lists
        for (int i = 0; i < n * n; i++)
        {
            Adj_Nodes[i] = new int[4];  // Each node can have up to 4 connections
            for (int j = 0; j < 4; j++)
            {
                Adj_Nodes[i][j] = -1;  // Initialize with -1 indicating no connection
            }
        }
    }

    //clean up dynamically allocated memory of adjacency list
    ~Grid_of_the_City()
    {
        //delete memory allocated for grid
        for (int i = 0; i < n; i++)
        {
            delete[] Grid[i];
        }
        delete[] Grid;
        //delete memory allocated for adjacency list
        for (int i = 0; i < n * n; i++)
        {
            delete[] Adj_Nodes[i];
        }
        delete[] Adj_Nodes;
    }
    //Method to setup the grid and adjacency list
    void Making_the_Grid()
    {
        int Node_ID = 1; // Start node ID from 1

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                Grid[i][j] = Node_ID;  //assign sequential IDs to grid nodes
                int index = 0;//index to keep track of the number of connections made to a node

                // Check and add valid connections (up, down, left, right)
                if (j > 0) Adj_Nodes[Node_ID - 1][index++] = Grid[i][j - 1]; // Left neighbor
                if (j < n - 1) Adj_Nodes[Node_ID - 1][index++] = Grid[i][j + 1]; // Right neighbor
                if (i > 0) Adj_Nodes[Node_ID - 1][index++] = Grid[i - 1][j]; // Top neighbor
                if (i < n - 1) Adj_Nodes[Node_ID - 1][index++] = Grid[i + 1][j]; // Bottom neighbor

                Node_ID++;
            }
        }
    }

    // Print the grid
    void Printing_the_Grid()
    {
        cout << "Grid Representation:" << endl;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                cout << setw(3) << Grid[i][j] << " ";
            }
            cout << endl;
            if (i < n - 1)
            {
                for (int j = 0; j < n; j++)
                {
                    cout << "--- ";
                }
                cout << endl;
            }
        }
    }



    // Function to convert grid coordinates to a single index
    int Get_ID_of_the_Node(int i, int j)
    {
        return i * n + j;
    }

    // Print adjacency lists
    void Printing_Adj_Nodes()
    {
        cout << "Adjacency List Representation:\n";
        for (int i = 0; i < n * n; i++)
        {
            cout << "node " << i + 1 << ": ";
            bool Connection = false; // Check if the node has any connections
            for (int j = 0; j < 4; j++)
            {
                if (Adj_Nodes[i][j] != -1)
                {
                    cout << Adj_Nodes[i][j] + 1 << " "; // Adjust index to match node numbering
                    Connection = true;
                }
            }
            if (!Connection) {
                cout << "No connections";
            }
            cout << endl;
        }
    }

    // Function to create nodes and edges for the graph
    void Making_the_Graph()
    {
        // Allocate memory for adjacency list
        Adj_Nodes = new int* [n * n];
        for (int i = 0; i < n * n; i++)
        {
            Adj_Nodes[i] = new int[4];  // Max 4 connections per node (up, down, left, right)
            for (int j = 0; j < 4; j++)
            {
                Adj_Nodes[i][j] = -1;  // Initialize with -1 indicating no connection
            }
        }

        // Create edges for each node
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                int node_id = Get_ID_of_the_Node(i, j);

                // Initialize index for connections
                int index_of_node = 0;

                // Check and add edges (up, down, left, right)
                if (j > 0) Adj_Nodes[node_id][index_of_node++] = Get_ID_of_the_Node(i, j - 1); // Left neighbor
                if (j < n - 1) Adj_Nodes[node_id][index_of_node++] = Get_ID_of_the_Node(i, j + 1); // Right neighbor
                if (i > 0) Adj_Nodes[node_id][index_of_node++] = Get_ID_of_the_Node(i - 1, j); // Top neighbor
                if (i < n - 1) Adj_Nodes[node_id][index_of_node++] = Get_ID_of_the_Node(i + 1, j); // Bottom neighbor
            }
        }
    }
    int bfs(int starting_node, int end)
    {
        int* distance_nodes = new int[n * n];
        memset(distance_nodes, -1, n * n * sizeof(int));
        int* queue = new int[n * n];
        int front = 0;
        int rear = 0;
        queue[rear++] = starting_node;
        distance_nodes[starting_node] = 0;

        while (front != rear)
        {
            int node = queue[front++];
            // Wrap around to use the queue as circular
            if (front == n * n) front = 0;
            for (int i = 0; i < 4; i++)
            {
                int node_neighbor = Adj_Nodes[node][i];
                if (node_neighbor != -1 && distance_nodes[node_neighbor] == -1)
                {
                    distance_nodes[node_neighbor] = distance_nodes[node] + 1;
                    queue[rear++] = node_neighbor;
                    if (node_neighbor == end) {
                        int total_distance = distance_nodes[node_neighbor];
                        delete[] distance_nodes;
                        delete[] queue;
                        return total_distance;
                    }
                }
            }
        }
        int total_distance = distance_nodes[end];
        delete[] distance_nodes;
        delete[] queue;
        // If there is no path from start to end, return a large number
        return total_distance == -1 ? INT_MAX : total_distance;
    }
    //function for in order traversal of the graph
    void InOrder_Traversal(int node, bool* visited)
    {
        //give proper working function
        visited[node] = true;
        for (int i = 0; i < 4; i++)
        {
            int neighbor = Adj_Nodes[node][i];
            if (neighbor != -1 && !visited[neighbor])
            {
                InOrder_Traversal(neighbor, visited);
            }

        }
    }
};
//input
struct Order
{
    string Item;
    string Location_of_Delivery;
    string Time_of_Delivery;
};

struct Restaurant
{
    string name;
    int Location_of_Node;
    int Number_of_Orders;
    Order* orders;
    //constructor
    Restaurant()
    {
        name = "";
        Location_of_Node = 0;
        Number_of_Orders = 0;
        orders = nullptr;
    }

};

const int Max_Orders = 5; // Maximum number of orders per rider

struct rider
{
    int Cur_Node;
    bool Free_Rider;
    int Free_Time;
    string assignedOrders[Max_Orders];
    int Number_of_Ass_Orders; // To keep track of the number of orders assigned

    //default constructor
    rider()
    {
        Cur_Node = 0;
        Free_Rider = true;
        Free_Time = 0;
        Number_of_Ass_Orders = 0;
    }
    // Constructor
    rider(int size_of_grid)
    {

        Cur_Node = rand() % (size_of_grid * size_of_grid);  // Generate a random location within the grid
        Free_Rider = true;
        Free_Time = 0;
        Number_of_Ass_Orders = 0;
    }
    // Assign orders to riders
    static void Orders_assigned(Restaurant* restaurants, int numRestaurants, rider* riders, int numRiders, Grid_of_the_City& city)
    {
        int Cur_Rider = 0;  // Start assigning orders to the first rider
        for (int i = 0; i < numRestaurants; i++)
        {
            for (int j = 0; j < restaurants[i].Number_of_Orders; j++)
            {
                if (riders[Cur_Rider].Number_of_Ass_Orders < Max_Orders)
                {
                    riders[Cur_Rider].assignedOrders[riders[Cur_Rider].Number_of_Ass_Orders++] = restaurants[i].orders[j].Location_of_Delivery;
                }
                // Move to the next rider, wrap around if necessary
                Cur_Rider = (Cur_Rider + 1) % numRiders;
            }
        }
    }

    // Calculate the best routes for all riders and assign the rider who is nearest to the restaurant
    static void Best_Route(rider* riders, int numRiders, Grid_of_the_City& city, int restaurantLocation)
    {

        int Minimum_Distance = INT_MAX;
        int Nearest_Rider = -1;

        for (int i = 0; i < numRiders; i++)
        {
            int Distance_to_Restaurant = city.bfs(riders[i].Cur_Node, restaurantLocation);
            if (Distance_to_Restaurant < Minimum_Distance)
            {
                Minimum_Distance = Distance_to_Restaurant;
                Nearest_Rider = i;
            }
        }

        if (Nearest_Rider != -1)
        {
            cout << "Rider " << (Nearest_Rider + 1) << " is nearest to the restaurant." << endl;
            // Assign orders to the nearest rider
            for (int j = 0; j < riders[Nearest_Rider].Number_of_Ass_Orders; j++)
            {
                int location = stoi(riders[Nearest_Rider].assignedOrders[j]);  // Convert string to integer
                int Route_Distance = city.bfs(riders[Nearest_Rider].Cur_Node, location);
                riders[Nearest_Rider].Cur_Node = location;  // Update rider's current location
                cout << "  To " << location << " distance: " << Route_Distance << " units" << endl;
            }
        }
    }

    // Calculate the total delivery time for all orders across all riders
    static int ToatL_Time_of_Delivery(rider* riders, int numRiders, Grid_of_the_City& city)
    {
        int Total_Time = 0;
        for (int i = 0; i < numRiders; i++)
        {
            for (int j = 0; j < riders[i].Number_of_Ass_Orders; j++)
            {
                int location = stoi(riders[i].assignedOrders[j]);  // Convert string to integer
                int time = city.bfs(riders[i].Cur_Node, location);
                Total_Time += time;
            }
        }
        return Total_Time;
    }
};

int main()
{
    Grid_of_the_City city;  // Initialize Gridcity with given size
    int TestCases;
t:
    cout << "Enter the number of test cases: ";
    cin >> TestCases;
    if (TestCases == 0)
    {
        cout << "invalid input. Enter something greater than 0" << endl;
        goto t;
    }

    for (int t = 0; t < TestCases; t++)
    {
    a:
        int n;
        cout << "Enter grid size n: ";
        cin >> n;

        if (n <= 0 || n == 1)
        {
            cout << "invalid grid size. Enter something greater than 1 and positive" << endl;
            goto a;
        }

        city.n = n;
        city.Set_Size_of_Grid();
        // Create graph based on the grid

        int num_of_riders = 5; // Total available riders

        int num_of_resturaunts;
    b:
        cout << "Enter number of restaurants: ";
        cin >> num_of_resturaunts;
        if (num_of_resturaunts == 0)
        {
            cout << "invalid input. Enter something greater than 0" << endl;
            goto b;
        }
        Restaurant* restaurants = new Restaurant[num_of_resturaunts];

        for (int i = 0; i < num_of_resturaunts; i++)
        {
        in:
            cout << "Enter the location for restaurant " << (i + 1) << ": ";
            cin >> restaurants[i].Location_of_Node;
            if (restaurants[i].Location_of_Node > n * n)
            {
                cout << "invalid input. Enter something in the range of 1 to " << n * n << endl;
                goto in;
            }

            cout << "Enter number of orders for " << restaurants[i].name << ": ";
            cin >> restaurants[i].Number_of_Orders;
            restaurants[i].orders = new Order[restaurants[i].Number_of_Orders];

            for (int j = 0; j < restaurants[i].Number_of_Orders; j++)
            {
            d:
                cout << "Enter delivery location for order " << (j + 1) << ": ";
                cin >> restaurants[i].orders[j].Location_of_Delivery;
                if (stoi(restaurants[i].orders[j].Location_of_Delivery) > n * n)
                {
                    cout << "incorrect input. Enter something in the range of 1 to " << n * n << endl;
                    goto d;
                }


            }
        }
        // Create the riders and assign random locations
        srand(time(0));
        rider* riders = new rider[num_of_riders];
        for (int i = 0; i < num_of_riders; i++)
        {
            riders[i] = rider(n);
            riders[i].Free_Rider = true;
            riders[i].Free_Time = 0;
        }
        // Display the random locations of the riders
        cout << "Rider locations:" << endl;
        for (int i = 0; i < num_of_riders; i++)
        {
            cout << "Rider " << (i + 1) << ": " << riders[i].Cur_Node << endl;
        }
        // Calculate the best routes for all riders
        for (int i = 0; i < num_of_resturaunts; i++)
        {
            for (int j = 0; j < restaurants[i].Number_of_Orders; j++)
            {
                int restaurantLocation = stoi(restaurants[i].orders[j].Location_of_Delivery);
                rider::Best_Route(riders, num_of_riders, city, restaurantLocation);
            }
        }
        //calling the function to assign orders to riders
        rider::Orders_assigned(restaurants, num_of_resturaunts, riders, num_of_riders, city);

        // Calculate the total delivery time for all orders across all riders
        int totalDeliveryTime = rider::ToatL_Time_of_Delivery(riders, num_of_riders, city);

        //int totalDeliveryTime = 0;
        for (int i = 0; i < num_of_resturaunts; i++)
        {
            for (int j = 0; j < restaurants[i].Number_of_Orders; j++)
            {
                int start = restaurants[i].Location_of_Node;
                int end = stoi(restaurants[i].orders[j].Location_of_Delivery);  // Assuming deliveryLocation is stored as string
                int deliveryTime = city.bfs(start - 1, end - 1);  // -1 to adjust for 0-based index
                totalDeliveryTime += deliveryTime;
            }
        }

        cout << "Total minimum delivery time for test case " << (t + 1) << ": " << totalDeliveryTime << " units." << endl;
        rider::Orders_assigned(restaurants, num_of_resturaunts, riders, num_of_riders, city);
        int totalDelivery = rider::ToatL_Time_of_Delivery(riders, num_of_riders, city);
        cout << "Total minimum delivery time: " << totalDelivery << " units." << endl;
        // Cleanup
        for (int i = 0; i < num_of_resturaunts; i++)
        {
            delete[] restaurants[i].orders;
        }
        delete[] restaurants;
    }


    city.Making_the_Grid();  // Setup grid nodes and adjacency lists
    //city.Making_the_Graph();
    city.Printing_the_Grid();
    city.Printing_Adj_Nodes();
    cout << "In-order traversal of the graph: ";
    city.InOrder_Traversal(0, new bool[city.n * city.n]);



    return 0;
}