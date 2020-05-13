import numpy as np
from matplotlib import pyplot as plt

#quadratic assignment problem
distance_matrix=np.array([[0,1,2,3,1,2,3,4],[1,0,1,2,2,1,2,3],[2,1,0,1,3,2,1,2],
                      [3,2,1,0,4,3,2,1],[1,2,3,4,0,1,2,3],[2,1,2,3,1,0,1,2],
                      [3,2,1,2,2,1,0,1],[4,3,2,1,3,2,1,0]])
flow_matrix=np.array([[0,5,2,4,1,0,0,6],[5,0,3,0,2,2,2,0],[2,3,0,0,0,0,0,5],
                      [4,0,0,0,5,2,2,10],[1,2,0,5,0,10,0,0],[0,2,0,2,10,0,5,1],
                      [0,2,0,2,0,5,0,10],[6,0,5,10,0,1,10,0]])

#cost function
def cost_function(distance,flow_matrix):
    cost=(distance*flow_matrix).sum()
    return cost


#dict btw  index and department name
convert={"A":0,
         "B":1,
         "C":2,
         "D":3,
         "E":4,
         "F":5,
         "G":6,
         "H":7}
#transform list of depeartment into distance matrix
def solution_function(solution):
    index_list=[]
    for each_letter in solution:
        index_list.append(convert[each_letter])
    new_solution= np.copy(distance_matrix)
    new_solution=new_solution[index_list,:]
    new_solution=new_solution[:,index_list]
    return new_solution

#calculate probability of accepting the bad move
def prob_function(a,b,current_temp):
    p=1/np.exp((a-b)/current_temp)
    return p

#move operator : generate new solution
def move(a):
    index_one=np.random.randint(0,len(a))
    index_two=np.random.randint(0,len(a))
    
    while index_one==index_two:
        index_two=np.random.randint(0,len(a))
    new_solution=np.copy(a)
    new_solution[index_one]=a[index_two]
    new_solution[index_two]=a[index_one]
    return new_solution


#hyper-parameter
temp=1500
M=250
N=20
alpha=0.9



############################start###########################################
loss_list=[]
temp_list=[]
solution_list=[]
#create initial solution
current_solution=np.array(["A","B","C","D","E","F","G","H"])
current_distance=solution_function(current_solution)
current_obj=cost_function(current_distance,flow_matrix)



for m in range(M):
    print(m," out of ",M)
    
    for n in range(N):
        #generate new solution
        new_solution=move(current_solution)
        new_distance=solution_function(new_solution)
        new_obj=cost_function(new_distance,flow_matrix)
 

        if new_obj<current_obj:
            #if new solution is better : take it
            current_solution=new_solution
            current_distance=new_distance
            current_obj=new_obj
        else:
            #if not : accept the worse solution with probability of acepting bad move
            rand=np.random.random()
            prob=prob_function(new_obj,current_obj,temp)
            if rand<=prob:
                current_solution=new_solution
                current_distance=new_distance
                current_obj=new_obj
            else:
                current_solution=current_solution
                current_distance=current_distance
                current_obj=current_obj  
    solution_list.append(current_solution)
    loss_list.append(current_obj)    
    #decrease temperature        
    temp=alpha*temp
    temp_list.append(temp)

best_index=np.argmin(loss_list)
optimal_solution=solution_list[best_index]
optimal_lost=loss_list[best_index]
print("best solution : ",optimal_solution)
print("best loss : ",optimal_lost)

#see result
plt.xlabel("m iteration")
plt.ylabel("loss")
plt.plot(np.arange(0,len(loss_list)),loss_list)














