# Copyright (c) 2024 ARM Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import (
    Param,
    VectorParam,
)
from m5.proxy import Parent
from m5.SimObject import SimObject


class BasePartitioningPolicy(SimObject):
    type = "BasePartitioningPolicy"
    cxx_header = "mem/cache/tags/partitioning_policies/base_pp.hh"
    cxx_class = "gem5::partitioning_policy::BasePartitioningPolicy"
    abstract = True


class WayPolicyAllocation(SimObject):
    type = "WayPolicyAllocation"
    cxx_header = "mem/cache/tags/partitioning_policies/way_allocation.hh"
    cxx_class = "gem5::partitioning_policy::WayPolicyAllocation"

    partition_id = Param.UInt64(
        "PartitionID to use the allocated ways" "Example: 0"
    )

    ways = VectorParam.UInt64(
        "Ways to be allocated to the provided PartitionID"
        "Format: [<way_num>,<way_num>, ...]"
        "Example: [0, 1]"
    )


class WayPartitioningPolicy(BasePartitioningPolicy):
    type = "WayPartitioningPolicy"
    cxx_header = "mem/cache/tags/partitioning_policies/way_pp.hh"
    cxx_class = "gem5::partitioning_policy::WayPartitioningPolicy"

    cache_associativity = Param.Unsigned(Parent.assoc, "Associativity")

    allocations = VectorParam.WayPolicyAllocation(
        "Array of WayPolicyAllocation objects, used to determine what will be"
        "done in each cache way"
        "Format: [<WayPolicyAllocation>,<WayPolicyAllocation>, ...]"
        "Example: ["
        "   WayPolicyAllocation(0, [0,1,2,3]),"
        "   WayPolicyAllocation(1, [4,5,6,7])"
        "]"
    )


class MaxCapacityPartitioningPolicy(BasePartitioningPolicy):
    type = "MaxCapacityPartitioningPolicy"
    cxx_header = "mem/cache/tags/partitioning_policies/max_capacity_pp.hh"
    cxx_class = "gem5::partitioning_policy::MaxCapacityPartitioningPolicy"

    cache_size = Param.MemorySize(Parent.size, "Cache size in bytes")
    blk_size = Param.Int(Parent.cache_line_size, "Cache block size in bytes")

    partition_ids = VectorParam.UInt64(
        "PartitionIDs assigned to this policy"
        "Format: [<partition_id>,<partition_id>, ...]"
        "Example: [0, 1]"
    )

    capacities = VectorParam.Float(
        "Assigned max capacity in range [0,1] for PartitionIDs"
        "(allocations rounded down to nearest cache block count)"
        "Format: [<max_capacity>,<max_capacity>,...]"
        "Example: [0.5, 0.75]"
    )
