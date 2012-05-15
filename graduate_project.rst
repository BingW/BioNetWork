============================================
酵母基因调控网络对外界环境刺激的因对系统研究
============================================

要求
1)	熟悉生物回路设计中各种网络模体功能和研究现状，并了解其中存在的问题；
2)	利用microarray产生的数据，分析不同环境变化情况下（例如，温度突变，高氧环境，还原性环境等）酵母基因的表达情况；
3)	构建基因表达调控模型，分析其鲁棒性，经济性和有效性并解释环境适应机制；

----
摘要
----
摘要：
关键词：酵母基因调控网络，网络模体，生物回路，鲁棒性，最优回路设计

--------
选题背景
--------

    进化的本质是生物体适应环境并将基因遗传传播开来。其中生物体如何适应环境又是其中最关键的问题。进化学家们相信基因的表达策略是生物体适应环境的关键。近年随着技术的发展，生物学家们使用基因表达的数量性状座位作图法(eQTL mapping)来揭示基因表达的差异的进化[1]；讨论全基因组加倍对物种适应能力的影响以及物种形成的影响[2]；还有优势突变的概率分布[3]等。这些都是从相对宏观的角度讨论种群的适应策略，对于个体的适应策略的研究则不多。同时，这些研究在机理方面的说明不足，只能给我们一个大致的方向，而各种机制则不明晰。于是我们有了系统生物学。
    
    系统生物学家的终极理想是解读生物体，甚至模拟生物体，即精确地计算出环境与基因组的输入对时间的输出函数。我们将这个函数称之为系统。比如布尔网络(Boolean Networks)[8]，有向图网络(directed network)[7]，贝叶斯网络(Bayesian Network)[9]以及动态贝叶斯网络[10]，微分方程(Ordinary Differential Equation)[11]，以及考虑了随机变量的Petri网络[16]和模糊Petri网络[17]等。
    
    本文采用的系统是酿酒酵母(Saccrharmoyces Serevisiae)，因为酵母是一种相对简单的单细胞生物，由于是真核生物，因此在后继的研究中应用价值更大。而且酵母也是一种工业用菌，因此研究酵母的应激(stress response)有利于提高生产效率。此外，酿酒酵母作为一个模式生物，其数据库也比较全，最有名的比如SGD(Saccharomyces Genome Datbase)[4], 还有搜集分析了数千份酵母表达谱(Microarray Expression Data)的SPELL[5]，以及专门研究位点的顺序的YGOB(Yeast Gene Order Browser)[6]等。因此选择酿酒酵母的应激系统作为对象研究"性价比"较高。


And there have many models [5-7]and experiments [7-10] exploring yeast’s response to the environmental change. 

Most of the models discussed the robustness [11-13]of the system but lack of balance with the other two dimensions: the effectiveness and the economy [14].

------------
过程设计论述
------------
    第一步是收集数据，然后构建出网络模型。


--------
结果分析
--------

--------
结论总结
--------

----
致谢
----

----
附录
----

--------
参考文献
--------

1. Evidence for widespread adaptive evolution of gene expression in budding yeast.PNAS 2010
2. The molecular evolutionary basis of species formation. Nature Reviews Genetics 2010
3. The population genetics of beneficial mutations. Philosophical Transactions of the Royal Society B-Biological Sciences 2010
4. SGD
5. SPELL
6. YGOB
7. Modeling and Simulation of Genetic Regulatory Systems: A Literature Review JCB 2002
8. Probabilistic Boolean Networks: A Rule-Based Uncertainty Model for Gene Regulatory Networks, Bioinformatics
9. Using Bayesian Networks to Analyze Expression Data, J. Computational Biology
10. Sensitivity and Specificity of Inferring Genetic Regulatory Interactions from Microarray Experiments with Dynamic Bayesian Networks, Bioinformatics
11. Search for Steady States of Piecewise-Linear Differential Equation Models of Genetic Regulatory Networks, IEEE/ACM Trans. Computational Biology and Bioinformatics, 
12. STEPP –search tool for exploration of Petri net paths: a new tool for Petri net-based path analysis in biochemical networks,
13. Designing Genetic Regulatory Networks Using Fuzzy Petri Nets Approach, International Journal of Automation and Computing, 
14.
