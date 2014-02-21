Gatheling
=========

Fledgeling prototype: The Gatherer

This is a software prototype to test some Fledgeling implementation ideas.
The parent project blog is here: http://blog.projectfledgeling.com/

Prototype goals (progress may be synchronous):
0. Create Specific Scenarios
    1. Character gathers food and water
    2. Tribe explores territory for food sources and farms
    3. Shop keeper accumulates wealth from obscure caches, communicates to locate them.

1. Implement a nested node framework
    1. Robust nested node structure
        1. Approximate number system?
        2. Automatic Parent transfer
        3. Property aggregation with caching
        4. Sub-object ejection when properties exceed parent capacity
    2. Node property interface
        1. Text based info readout and entry
            1. Level of Depth limitation
            2. Approximate Quantity/Quality descriptors? (are approximate numbers good enough?)
        2. Node search?
        3. Node Address System?
2. Implement a working ideaspace containing essentials for characters
    1. character qualities
    2. verb qualities
    3. noun qualities
    4. Approximate descriptors? Metaphors? Is this automatic?
3. Implement a working instance/concrete space containing essentials for character interactions
    1. Implement a history/memory model which allows characters to move and consume resources
    2. Implement a desire/plan model which allows characters to form and constructively act on goals
    3. Implement a communication model which allows characters to transfer memories and goals
        1. Multi-character "simultaneous" processing? Do we get this for free with nesting?
        2. Subscription and notification?
        3. Language?
4. Graphical Interface?
    1. Node Structure Explorer
    2. Node visualization
    3. Node creation/alteration

Other ideas? Things I missed?
