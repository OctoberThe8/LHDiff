// Source - https://codereview.stackexchange.com/a
// Posted by Steephen
// Retrieved 2025-11-29, License - CC BY-SA 3.0

#include<iostream>
#include<algorithm>
#include<unordered_map>
#include<array>
#include<type_traits>

template <typename T1, std::size_t N>
std::unordered_map<int,int> count_frequency(std::array<T1,N> & array)
{
    std::unordered_map<int,int> temp_unordered_map;
    auto temp_unordered_map_end = std::end(temp_unordered_map);
    for( auto &x: array)
    {
        auto it_temp_unordered_map = temp_unordered_map.find(x);
        if( it_temp_unordered_map == temp_unordered_map_end)
        {
            temp_unordered_map.emplace(x,1);                       
        }
        else
        {
            ++(it_temp_unordered_map->second);
        }
    }
    return temp_unordered_map;
}

template <typename T1, std::size_t N1, std::size_t N2>
bool is_permutation(std::array<T1,N1> & array1, std::array<T1,N2>&  array2)
{       
    static_assert(N1==N2, "is_permutation accepts same size arrays");   

    std::unordered_map<int,int> first_map = count_frequency(array1);        
    std::unordered_map<int,int> second_map = count_frequency(array2);

    std::pair<std::unordered_map<int,int>::iterator,std::unordered_map<int,int>::iterator> myPair=
        std::mismatch(std::begin(first_map),std::end(first_map),std::begin(second_map), 
        [](std::pair<const int,int>& seed1, std::pair<const int,int> & seed2) 
        { return seed1.second == seed2.second;}
        );

    return  myPair.first == first_map.end() && myPair.second == second_map.end(); 
}

int main()
{     
    std::array<int,4> array1 {{1,3,1,4}};
    std::array<int,4> array2 {{1,1,4,3}};

    if(::is_permutation<int,array1.size(), array2.size()>(array1, array2))
        std::cout<< " Arrays are permutation of each other\n"; 
    else
        std::cout<< " Arrays are not permutation of each other\n";

    return 0;
}
