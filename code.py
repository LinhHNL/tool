import math
import random
import time

# Hàm tính khoảng cách Euclidean giữa hai điểm có tọa độ (x1, y1) và (x2, y2)
def eud_dis(x1, y1, x2, y2):
    """
    Input:
        x1: float
            Tọa độ x của thành phố bắt đầu trong không gian Euclidean
        y1: float
            Tọa độ y của thành phố bắt đầu trong không gian Euclidean
        x2: float
            Tọa độ x của thành phố kết thúc trong không gian Euclidean
        y2: float
            Tọa độ y của thành phố kết thúc trong không gian Euclidean
    Output:
        float: Số thực biểu diễn khoảng cách của đường đi giữa thành phố bắt đầu và thanh phố kết thúc trong không gian Euclidean 2 chiều
    """
    # Tính khoảng cách d trong không gian Euclidean 2 chiều theo công thức sqrt((x1-x2)^2 + (y1-y2)^2)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Hàm tính fitness của một hành trình trên đồ thị
def calculate_fitness(graph, org_tour):
    """
    Input:
        Graph: list
            Mảng 2 chiều biểu diễn đồ thị của bài toán theo dạng [[x1, y1], [x2, y2], ..., [xn, yn]], với mỗi cặp (x, y) là tọa độ của một thành phố
        org_hawk: list
            Mảng một chiều biểu diễn đường đi của trong không gian rời rạc
    Output:
        float: Số thực biểu diễn khoảng cách của đường đi đầu vào
    """

    # Khởi tạo fitness ban đầu
    fitness = 0
    # Biến đổi hành trình sang biểu diễn mã khóa ngẫu nhiên
    tour = random_key_encode(org_tour)

    # Duyệt qua từng thành phố trong hành trình để tính khoảng cách
    for city in range(len(tour) - 1):
        x1, y1 = graph[tour[city]]
        x2, y2 = graph[tour[city + 1]]
        fitness += eud_dis(x1, y1, x2, y2)

    return fitness
   
def random_key_encode(tour):
    """
    Input:
        tour: list
            Mảng một chiều biểu diễn đường đi của trong không gian liên tục
    Output:
        list: Mảng một chiều biểu diễn đường đi của trong không gian rời rạc
    """
    # Sắp xếp lại vị trí của thành phố theo trọng số tương ứng
    return sorted(range(len(tour)), key=lambda c: tour[c])


#Tính LF(x) theo công thức 9 với đầu vào là dim là kích thước  của mỗi hawk
def levy_flight(dim):

    beta = 1.5
    #gán beta =1.5 là giá trị default của nó
    #Tính sigma
    sigma = ((math.gamma(1 + beta) * math.sin(math.pi * beta / 2)) / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    #Tính mỗi giá trị 0.01*u*sigma
    usigma = [0.01 * random.gauss(0, 1) * sigma for _ in range(dim)]
    #Tính mỗi giá trị ngầu nhiên của v với kích thước dim
    v = [random.gauss(0, 1) for _ in range(dim)]
    #Tính mỗi giá trị |v|*1/beta
    zz = [abs(value) ** (1 / beta) for value in v]
    #Tính mỗi giá trị LF(x)

    step = [usigma[i] / zz[i] for i in range(dim)]
    return step


#Tính giá trị của Z theo công thức 8
#Với D là dim là kích thước của hawk
#Với Y 
def dive(Y, D):
    S = [random.random() for _ in range(D)]
    LF = levy_flight(D)
    Z = [Y[i] + S[i] * LF[i] for i in range(D)]
    return Z



"""
Input:
        Graph: list
            Một mảng 2 chiều biểu diễn đồ thị của bài toán theo dạng [[x1, y1], [x2, y2], ..., [xn, yn]], với mỗi cặp (x, y) là tọa độ của một thành phố
        N: integer
            Số lượng hawk/tour sẽ tìm đường đi tối ưu
        T: integer
            Số vòng lặp để thực hiện thuật toán
        dim: là kích thước của đồ thị
        LB: là giới hạn trên 
        UB: là giớn hạn dưới
    Output:
        X_rabbit: list
            Một mảng một chiều biểu diễn đường đi tối ưu nhất mà thuật toán tìm được theo dạng [c0, c1, c2, ..., cn], với ci là thành phố thứ i
        best_fitness : tổng đường đi tốt nhất tìm được
"""
def HHO(graph, N, T, dim, LB, UB):
    # Khởi tạo N hawk/tour/solution ngẫu nhiên
    X = [[random.random() for _ in range(len(graph))] for _ in range(N)]
        # Khởi tạo các giá trị để tính tour có fitness tốt nhất
    Xrabbit = []
    best_fitness = float('inf')
    t = 0

    while t < T:
        # Kiểm tra từng hawk        
        for i in range(N):
            hawk = i
            # Tính fitness của hawk hiện tại
            fitness = calculate_fitness(graph, X[hawk])
            # Nếu hawk hiện tại có fitness tốt hơn thì cập nhất X_rabbit thành hawk hiện tại
            if fitness < best_fitness:
                best_fitness = fitness
                Xrabbit = X[hawk]
        #Chạy vòng lặp để chạy qua tất cả các phần tử trong X
        for i in range(N):
            # Khởi tạo năng lượng ban đầu
            E0 = 2 * random.random() - 1
            # Khởi tạo sức nhảy J
            J = 2 * (1 - random.random())
            # Cập nhật năng lượng, năng lượng sẽ giảm dần đến < 1 để vào giai đoạn exploitation Eq(3)
            E = 2 * E0 * (1 - (t / T))
            abs_E = abs(E)
            # Vào giai đoạn EXPLORATION sử dụng Eq(1)
            if abs_E >= 1:
                # Khởi tạo giá trị ngẫu nhiên q để lựa chọn chiến lược sử dụng
                q = random.random()

                Xrand_Hawk_index = random.randint(0, N - 1)
                #Tính vị trí trung bình của các hawl
                average_location = [sum(x) / N for x in zip(*X)]

                if q >= 0.5:
                    #Nếu q>=0.5 thì sử dụng công thức Xrand(t) - r1|Xrand(t) -2r2X(t)| để tính vị trí mới của hawk
                    X[i] = [X[Xrand_Hawk_index][j] - random.random() * abs(X[Xrand_Hawk_index][j] - 2 * random.random() * X[i][j]) for j in range(len(X[i]))]
                else:
                     #Nếu q>=0.5 thì sử dụng công thức (Xrabbit(t) - Xm(t))-r3(LB + r4(UB-LB)) để tính vị trí mới của hawk
                    X[i] = [(Xrabbit[j] - average_location[j]) - random.random() * (LB + random.random() * (UB - LB)) for j in range(len(X[i]))]
                    #Trong đó :
                    #           r1,r2,r3,r4 là các số ngẫu nhiên trong khoảng từ 0 đến 1
                    #           LB và UB là giới hạn trên và giới hạn dưới
                    #           Xrabbit là vị trí rabbit tốt nhất
                    #           Xrand là vị trí ngẫu nhiên của hawk
                    #           Xm là vị trí trung bình của hawk
            else:
                r = random.random()
                # Khởi tạo giá trị ngẫu nhiên r để lựa chọn chiến lược sử dụng

                if r >= 0.5 and abs_E >= 0.5:
                    #Với r>=0.5 và |E| >= 0.5 thì sử dụng Eq(4)
                    X[i] = [(Xrabbit[j] - X[i][j] - E * abs(J * Xrabbit[j] - X[i][j])) for j in range(len(X[i]))]
                elif r >= 0.5 and abs_E < 0.5:
                    #Với r>=0.5 và |E| < 0.5 thì sử dụng Eq(6)

                    X[i] = [(Xrabbit[j] - E * abs(Xrabbit[j] - X[i][j])) for j in range(len(X[i]))]
                elif r < 0.5 and abs_E >= 0.5:
                    #Với r<0.5 và |E| >= 0.5 thì sử dụng Eq(10)

                    Y = [(Xrabbit[j] - E * abs(J*Xrabbit[j] - X[i][j])) for j in range(len(X[i]))]
                    #Tính Y theo công thức (7)
                    Z = dive(Y, dim)
                    #Tính Z theo công thức (8) 

                    #So sánh fitness của Y và X(i) nếu Y tốt hơn thì gán X(i) là Y
                    if calculate_fitness(graph, Y) < calculate_fitness(graph, X[i]):
                        X[i] = Y
                    #So sánh fitness của Z và X(i) nếu Z tốt hơn thì gán X(i) là Z
                        
                    elif calculate_fitness(graph, Z) < calculate_fitness(graph, X[i]):
                        X[i] = Z
                    
                elif r < 0.5 and abs_E < 0.5:
                    #Với r<0.5 và |E| < 0.5 thì sử dụng Eq(11)

                    Y = [(Xrabbit[j] - E * abs(J * Xrabbit[j] - X[i][j])) for j in range(len(X[i]))]
                    #Tính Y theo công thức (12)

                    Z = dive(Y, dim)
                    #Tính Z theo công thức (13)

                    #So sánh fitness của Y và X(i) nếu Y tốt hơn thì gán X(i) là Y

                    if calculate_fitness(graph, Y) < calculate_fitness(graph, X[i]):
                        X[i] = Y
                    #So sánh fitness của Z và X(i) nếu Z tốt hơn thì gán X(i) là Z

                    elif calculate_fitness(graph, Z) < calculate_fitness(graph, X[i]):
                        X[i] = Z
        t = t + 1

    return Xrabbit, best_fitness


