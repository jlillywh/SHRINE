graph [
    version 1.000
    Creator "Jason Lillywhite"
    directed 1

    comment "This is a graph representation of a watershed"
    directed 1
    id 42
    label "Watershed Input File"
    node [
        id 201
        label "C1"
        node_type 200
    ]
    node [
        id 202
        label "C2"
        node_type 200
    ]
    node [
        id 203
        label "C3"
        node_type 200
    ]
    node [
        id 204
        label "C4"
        node_type 200
    ]
    node [
        id 205
        label "C5"
        node_type 200
    ]
    node [
        id 206
        label "C6"
        node_type 200
    ]
    node [
        id 301
        label "J1"
        node_type 300
    ]
    node [
        id 302
        label "J2"
        node_type 300
    ]
    node [
        id 303
        label "J3"
        node_type 300
    ]

    edge [
        source 201
        target 301
        label "Flow from node C1 to node J1"
    ]
    edge [
        source 202
        target 301
        label "Flow from node C2 to node J1"
    ]
    edge [
        source 203
        target 302
        label "Flow from node C3 to node J2"
    ]
    edge [
        source 204
        target 302
        label "Flow from node C4 to node J2"
    ]
    edge [
        source 205
        target 303
        label "Flow from node C5 to node J3"
    ]
    edge [
        source 206
        target 303
        label "Flow from node C6 to node J3"
    ]

    edge [
        source 302
        target 301
        label "Flow from node J2 to node J1"
        runoff 9.0e99
    ]

    edge [
        source 303
        target 302
        label "Flow from node J3 to node J2"
        runoff 9.0e99
    ]

]