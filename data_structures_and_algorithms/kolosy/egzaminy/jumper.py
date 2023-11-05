#TIME: O(V^3), #SPACE: O(n)

def jumper(G, s, w):
    def dijkstra(G, s ,t):
        n = len(G)
        dist = [[float("inf"), float("inf")] for _ in range(n)]
        visited = [[False, False] for _ in range(n)]
        dist[s][0] = 0
        dist[s][1] = 0

        for _ in range(2*n):
            val_u = dist[0][0]
            u_1 = 0
            u_2 = 0
            flag = False
            for v_1 in range(n):
                if flag: break
                for v_2 in range(2):
                    if not visited[v_1][v_2]:
                        val_u = dist[v_1][v_2]
                        u_1 = v_1
                        u_2 = v_2
                        flag = True
                        break
            
            for v_1 in range(n):
                for v_2 in range(2):
                    if visited[v_1][v_2] == False and dist[v_1][v_2] <= val_u:
                        u_1 = v_1
                        u_2 = v_2
                        val_u = dist[v_1][v_2]

            visited[u_1][u_2] = True

            for v in range(n):
                if G[u_1][v] > 0 and not visited[v][1] and dist[v][1] > dist[u_1][u_2] + G[u_1][v]:
                    dist[v][1] = dist[u_1][u_2] + G[u_1][v]
                
                if u_2 == 1:
                    if G[u_1][v] > 0:
                        for v_2 in range(n):
                            if G[v][v_2] > 0 and not visited[v_2][0] and dist[v_2][0] > dist[u_1][u_2] + max(G[u_1][v], G[v][v_2]):
                                dist[v_2][0] = dist[u_1][u_2] + max(G[u_1][v], G[v][v_2])


        return min(dist[t][0], dist[t][1])

    res =dijkstra(G, s, w)

    return res
