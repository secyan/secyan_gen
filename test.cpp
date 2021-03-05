enum RelationName
{
    CUSTOMER,
    ORDERS,
    LINEITEM,
    PART,
    SUPPLIER,
    PARTSUPP,
    RTOTAL
};

size_t NumRows[RTOTAL][DTOTAL] = {
	{150, 450, 1500, 4950, 15000},
	{1500, 4500, 15000, 49500, 150000},
	{6005, 17973, 60175, 198344, 595215},
	{200, 600, 2000, 6600, 20000},
	{10, 30, 100, 330, 1000},
	{800, 2400, 8000, 26400, 80000}};

void run_Demo(DataSize ds, bool printResult){
    auto customer_ri = {
            SERVER,
    		false,
    		{ "c_custkey" },
    		{ Relation::INT },
    		NumRows[rn][ds],
    		false
    };
    Relation::AnnotInfo customer_ai = {true, true};
    Relation orders(customer_ri, customer_ai);
    filePath = GetFilePath(CUSTOMER, ds);
    customer.LoadData(filePath.c_str(), "demo");
    
    auto orders_ri = {
            SERVER,
    		false,
    		{ "o_custkey","o_orderkey" },
    		{ Relation::INT,Relation::INT },
    		NumRows[rn][ds],
    		false
    };
    Relation::AnnotInfo orders_ai = {true, true};
    Relation orders(orders_ri, orders_ai);
    filePath = GetFilePath(ORDERS, ds);
    orders.LoadData(filePath.c_str(), "demo");
    
    auto lineitem_ri = {
            SERVER,
    		false,
    		{ "l_orderkey" },
    		{ Relation::INT },
    		NumRows[rn][ds],
    		false
    };
    Relation::AnnotInfo lineitem_ai = {true, true};
    Relation orders(lineitem_ri, lineitem_ai);
    filePath = GetFilePath(LINEITEM, ds);
    lineitem.LoadData(filePath.c_str(), "demo");
    
    customer.SemiJoin(orders,c_custkey , o_custkey);
    lineitem.SemiJoin(orders,l_orderkey , o_orderkey);
    
    lineitem.RevealAnnotToOwner();
    if (printResult)
        lineitem.Print();
}