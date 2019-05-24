graph [
    version 1.000
    Creator "Jason Lillywhite"
    directed 1
    id 42
    label "Network Input File"
    node [
        id 1
        label "C1"
        node_type "Catchment"
    ]
    node [
        id 2
        label "C2"
        node_type "Catchment"
    ]
    node [
        id 3
        label "C3"
        node_type "Catchment"
    ]
    node [
        id 4
        label "C4"
        node_type "Catchment"
    ]
    node [
        id 5
        label "J1"
        node_type "Junction"
    ]
    node [
        id 6
        label "J2"
        node_type "Junction"
    ]
    node [
        id 7
        label "Sink"
    ]
    edge [
        source 1
        target 5
        capacity 0.0
        label "Flow from node C1 to node J1"
    ]
    edge [
        source 2
        target 5
        capacity 0.0
        label "Flow from node C2 to node J1"
    ]
    edge [
        source 3
        target 6
        capacity 0.0
        label "Flow from node C3 to node J2"
    ]
    edge [
        source 4
        target 6
        capacity 0.0
        label "Flow from node C4 to node J2"
    ]
    edge [
        source 5
        target 6
        label "Flow from node J1 to node J2"
    ]
    edge [
        source 6
        target 7
        label "Flow from node J2 to Sink"
    ]
]