#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "DirectedGraph.h"

void LoadDGraph(char *fname,DirectedGraph *G)
{
   	int i,N,st,end;
	FILE *fp = fopen(fname,"r");
	if (fp==NULL) {
		printf("Opening file %s failed.\n",fname);
		exit(1);
	}
	
	/* Read the number of teams N */
	fscanf(fp,"%d\n",&N);    
    Initialize(G,N);
	while (fscanf(fp,"%d-%d\n",&st,&end)==2) 
    {
        InsertEdge(G,st,end);   
    }
	fclose (fp);
}

Boolean containsCycle(DirectedGraph G)
{
    int i;
    for (i=0; i<G.n; i++) 
    {
        Edge *e=G.firstedge[i];
        while (e) 
        {
            if (e->eclass==Back) 
                return TRUE;
            e = e->nextedge;
        }
    }
    return FALSE;    
}

void simple_test() 
{
    DirectedGraph G;
    Initialize(&G,5);
    printf("n=%d\n",G.n);
    InsertEdge(&G,0,1);
    InsertEdge(&G,0,2);
    InsertEdge(&G,1,3);
    InsertEdge(&G,4,2);
    InsertEdge(&G,4,3);

    ShowGraph(G);

}

int main(int argc,char **argv) 
{
    int i;
    if (argc!=2)
    {
        printf("Syntax: %s file_name\n",argv[0]);
        exit(0);
    }

    
    DirectedGraph G;
    printf("Loading graph from file %s\n",argv[1]);
    LoadDGraph(argv[1],&G);
    printf("\nThe graph is:\n");
    ShowGraph(G);
    
    printf("\nDFS-based edge classification:\n");
    DepthFirst(G);
    printEdges(&G);
    
    if (containsCycle ( G ) == FALSE) 
    {   
        printf("\nTopological order\n");     
        Toporder Topo;  
        BreadthTopSort(G,Topo);
        for (i=0; i<G.n;i++)
            printf("T[%d]=%d\n",i,Topo[i]);
    }
    else {
        printf("\nG contains a cycle (so no topological order)\n");
    }

    printf("\nReverse of G\n");
    DirectedGraph *rG;
    rG = GraphReverse(G);
    ShowGraph(*rG);

    printf("\nStrongly Connected Components\n");
    int *sc = StrongComponents(G);
    for (i=0; i<G.n; i++)
        if (sc[i]!=-1)
            printf("SC[%d]=%d\n",i,sc[i]);
}
