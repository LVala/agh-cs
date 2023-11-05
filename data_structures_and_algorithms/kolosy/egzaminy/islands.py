# TIME: O(V^2), SPACE: O(n)
# wg testów działa, ale były tylko jakieś 2 proste

def islands(G, A, B):
    def dijkstra(G, s ,t):
        n = len(G)
        dist = [[float("inf"),float("inf"),float("inf")] for _ in range(n)]
        visited = [[False,False,False] for _ in range(n)]
        dist[s][0] = 0
        dist[s][1] = 0
        dist[s][2] = 0

        for _ in range(3*n):
            val_u = dist[0][0]
            u_1 = 0
            u_2 = 0
            flag = False
            for v_1 in range(n):
                if flag: break
                for v_2 in range(3):
                    if not visited[v_1][v_2]:
                        val_u = dist[v_1][v_2]
                        u_1 = v_1
                        u_2 = v_2
                        flag = True
                        break
            
            for v_1 in range(n):
                for v_2 in range(3):
                    if visited[v_1][v_2] == False and dist[v_1][v_2] <= val_u:
                        u_1 = v_1
                        u_2 = v_2
                        val_u = dist[v_1][v_2]

            visited[u_1][u_2] = True

            for v_1 in range(n):
                if G[u_1][v_1] > 0:
                    for v_2 in range(3):
                        if visited[v_1][v_2] == False and u_2 != v_2 and dist[v_1][v_2] > dist[u_1][u_2] + G[u_1][v_1]:
                            dist[v_1][v_2] = dist[u_1][u_2] + G[u_1][v_1]

        return min(dist[t][0], dist[t][1], dist[t][2])
    
    res = dijkstra(G, A, B)
    return res
