

TEST_CONFIG = [
    {
        "table_name": "SUPPLIER",
        "data_sizes": [
            10,
            30,
            100,
            330,
            1000
        ],
        "data_paths":
            ["a", "a", "a", "a", "a"],
        "columns": [
            {
                "column_type": "int",
                "name": "s_suppkey"
            },
            {
                "column_type": "string",
                "name": "s_name"
            },
            {
                "column_type": "string",
                "name": "s_address"
            },
            {
                "column_type": "string",
                "name": "s_nationkey"
            },
            {
                "column_type": "string",
                "name": "s_phone"
            },
            {
                "column_type": "decimal",
                "name": "s_acctbal"
            },
            {
                "column_type": "string",
                "name": "s_comment"
            }
        ]
    },
    {
        "table_name": "CUSTOMER",
        "data_sizes": [
            150,
            450,
            1500,
            4950,
            15000
        ],
        "data_paths":
            ["a", "a", "a", "a", "a"],
        "columns": [
            {
                "column_type": "int",
                "name": "c_custkey"
            },
            {
                "column_type": "string",
                "name": "c_name"
            },
            {
                "column_type": "string",
                "name": "c_address"
            },
            {
                "column_type": "string",
                "name": "c_nationkey"
            },
            {
                "column_type": "string",
                "name": "c_phone"
            },
            {
                "column_type": "decimal",
                "name": "c_acctbal"
            },
            {
                "column_type": "string",
                "name": "c_mktsegment"
            },
            {
                "column_type": "string",
                "name": "c_comment"
            }
        ]
    },
    {
        "table_name": "LINEITEM",
        "data_sizes": [
            6005,
            17973,
            60175,
            198344,
            595215
        ],
        "data_paths":
            ["a", "a", "a", "a", "a"],
        "columns": [
            {
                "column_type": "int",
                "name": "l_orderkey"
            },
            {
                "column_type": "int",
                "name": "l_partkey"
            },
            {
                "column_type": "int",
                "name": "l_suppkey"
            },
            {
                "column_type": "int",
                "name": "l_linenumber"
            },
            {
                "column_type": "decimal",
                "name": "l_quantity"
            },
            {
                "column_type": "decimal",
                "name": "l_extendedprice"
            },
            {
                "column_type": "decimal",
                "name": "l_discount"
            },
            {
                "column_type": "decimal",
                "name": "l_tax"
            },
            {
                "column_type": "string",
                "name": "l_returnflag"
            },
            {
                "column_type": "string",
                "name": "l_linestatus"
            },
            {
                "column_type": "date",
                "name": "l_shipdate"
            },
            {
                "column_type": "date",
                "name": "l_commitdate"
            },
            {
                "column_type": "date",
                "name": "l_receiptdate"
            },
            {
                "column_type": "string",
                "name": "l_shippinstruct"
            },
            {
                "column_type": "string",
                "name": "l_shipmode"
            },
            {
                "column_type": "string",
                "name": "l_comment"
            }
        ]
    },
    {
        "table_name": "ORDERS",
        "data_sizes": [
            1500,
            4500,
            15000,
            49500,
            150000
        ],
        "data_paths":
            ["a", "a", "a", "a", "a"],
        "columns": [
            {
                "column_type": "int",
                "name": "o_orderkey"
            },
            {
                "column_type": "int",
                "name": "o_custkey"
            },
            {
                "column_type": "string",
                "name": "o_orderstatus"
            },
            {
                "column_type": "string",
                "name": "o_totalprice"
            },
            {
                "column_type": "date",
                "name": "o_orderdate"
            },
            {
                "column_type": "string",
                "name": "o_orderpriority"
            },
            {
                "column_type": "string",
                "name": "o_clerk"
            },
            {
                "column_type": "int",
                "name": "o_shippriority"
            },
            {
                "column_type": "string",
                "name": "o_comment"
            }
        ]
    },
    {
        "table_name": "REGION",
        "data_sizes": [],
        "data_paths":
            [],
        "columns": [
            {
                "column_type": "int",
                "name": "r_regionkey"
            },
            {
                "column_type": "string",
                "name": "r_name"
            },
            {
                "column_type": "string",
                "name": "r_comment"
            }
        ]
    },
    {
        "table_name": "nation",
        "data_sizes": [],
        "data_paths":
            [],
        "columns": [
            {
                "column_type": "int",
                "name": "n_nationkey"
            },
            {
                "column_type": "string",
                "name": "n_name"
            },
            {
                "column_type": "string",
                "name": "n_regionkey"
            },
            {
                "column_type": "string",
                "name": "n_comment"
            }
        ]
    },
    {
        "table_name": "part",
        "data_sizes": [
            200,
            600,
            2000,
            6600,
            20000
        ],
        "data_paths":
            ["a", "a", "a", "a", "a"],
        "columns": [
            {
                "column_type": "int",
                "name": "p_partkey"
            },
            {
                "column_type": "string",
                "name": "p_name"
            },
            {
                "column_type": "string",
                "name": "p_mfgr"
            },
            {
                "column_type": "string",
                "name": "p_brand"
            },
            {
                "column_type": "string",
                "name": "p_type"
            },
            {
                "column_type": "int",
                "name": "p_size"
            },
            {
                "column_type": "string",
                "name": "p_container"
            },
            {
                "column_type": "decimal",
                "name": "p_retailprice"
            },
            {
                "column_type": "string",
                "name": "p_comment"
            }
        ]
    },
    {
        "table_name": "partsupp",
        "data_sizes": [
            800,
            2400,
            8000,
            26400,
            80000
        ],
        "data_paths":
            ["a", "a", "a", "a", "a"],
        "columns": [
            {
                "column_type": "int",
                "name": "ps_partkey"
            },
            {
                "column_type": "int",
                "name": "ps_suppkey"
            },
            {
                "column_type": "int",
                "name": "ps_availqty"
            },
            {
                "column_type": "decimal",
                "name": "ps_supplycost"
            },
            {
                "column_type": "string",
                "name": "ps_comment"
            }
        ]
    }
]

TEST_DB_PLAN = [
    {
        "Plan": {
            "Node Type": "Limit",
            "Parallel Aware": False,
            "Startup Cost": 26480.7,
            "Total Cost": 26480.75,
            "Plan Rows": 20,
            "Plan Width": 59,
            "Plans": [
                {
                    "Node Type": "Sort",
                    "Parent Relationship": "Outer",
                    "Parallel Aware": False,
                    "Startup Cost": 26480.7,
                    "Total Cost": 26518.2,
                    "Plan Rows": 15000,
                    "Plan Width": 59,
                    "Sort Key": [
                        "(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))) DESC"
                    ],
                    "Plans": [
                        {
                            "Node Type": "Aggregate",
                            "Strategy": "Hashed",
                            "Partial Mode": "Simple",
                            "Parent Relationship": "Outer",
                            "Parallel Aware": False,
                            "Startup Cost": 25894.05,
                            "Total Cost": 26081.55,
                            "Plan Rows": 15000,
                            "Plan Width": 59,
                            "Group Key": [
                                "customer.c_custkey",
                                "customer.c_name",
                                "customer.c_nationkey"
                            ],
                            "Plans": [
                                {
                                    "Node Type": "Hash Join",
                                    "Parent Relationship": "Outer",
                                    "Parallel Aware": False,
                                    "Join Type": "Inner",
                                    "Startup Cost": 9547.96,
                                    "Total Cost": 25563.27,
                                    "Plan Rows": 22052,
                                    "Plan Width": 39,
                                    "Inner Unique": False,
                                    "Hash Cond": "(orders.o_custkey = customer.c_custkey)",
                                    "Plans": [
                                        {
                                            "Node Type": "Gather",
                                            "Parent Relationship": "Outer",
                                            "Parallel Aware": False,
                                            "Startup Cost": 8153.96,
                                            "Total Cost": 23893.62,
                                            "Plan Rows": 11026,
                                            "Plan Width": 16,
                                            "Workers Planned": 2,
                                            "Single Copy": False,
                                            "Plans": [
                                                {
                                                    "Node Type": "Hash Join",
                                                    "Parent Relationship": "Outer",
                                                    "Parallel Aware": True,
                                                    "Join Type": "Inner",
                                                    "Startup Cost": 7153.96,
                                                    "Total Cost": 21791.02,
                                                    "Plan Rows": 4594,
                                                    "Plan Width": 16,
                                                    "Inner Unique": False,
                                                    "Hash Cond": "(lineitem.l_orderkey = orders.o_orderkey)",
                                                    "Plans": [
                                                        {
                                                            "Node Type": "Seq Scan",
                                                            "Parent Relationship": "Outer",
                                                            "Parallel Aware": True,
                                                            "Relation Name": "lineitem",
                                                            "Alias": "lineitem",
                                                            "Startup Cost": 0.0,
                                                            "Total Cost": 14386.98,
                                                            "Plan Rows": 61584,
                                                            "Plan Width": 16,
                                                            "Filter": "(l_returnflag = 'R'::bpchar)"
                                                        },
                                                        {
                                                            "Node Type": "Hash",
                                                            "Parent Relationship": "Inner",
                                                            "Parallel Aware": True,
                                                            "Startup Cost": 7095.0,
                                                            "Total Cost": 7095.0,
                                                            "Plan Rows": 4717,
                                                            "Plan Width": 8,
                                                            "Plans": [
                                                                {
                                                                    "Node Type": "Seq Scan",
                                                                    "Parent Relationship": "Outer",
                                                                    "Parallel Aware": True,
                                                                    "Relation Name": "orders",
                                                                    "Alias": "orders",
                                                                    "Startup Cost": 0.0,
                                                                    "Total Cost": 7095.0,
                                                                    "Plan Rows": 4717,
                                                                    "Plan Width": 8,
                                                                    "Filter": "((o_orderdate >= '1993-08-01'::date) AND (o_orderdate < '1993-11-01 00:00:00'::timestamp without time zone))"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "Node Type": "Hash",
                                            "Parent Relationship": "Inner",
                                            "Parallel Aware": False,
                                            "Startup Cost": 1019.0,
                                            "Total Cost": 1019.0,
                                            "Plan Rows": 30000,
                                            "Plan Width": 27,
                                            "Plans": [
                                                {
                                                    "Node Type": "Seq Scan",
                                                    "Parent Relationship": "Outer",
                                                    "Parallel Aware": False,
                                                    "Relation Name": "customer",
                                                    "Alias": "customer",
                                                    "Startup Cost": 0.0,
                                                    "Total Cost": 1019.0,
                                                    "Plan Rows": 30000,
                                                    "Plan Width": 27
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
]
