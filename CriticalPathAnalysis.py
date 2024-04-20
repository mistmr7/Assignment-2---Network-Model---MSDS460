# Critical Path Analysis

# Problem description from Williams (2013, pages 95-98)
# Williams, H. Paul. 2013. Model Building in Mathematical Programming (fifth edition). New York: Wiley. [ISBN-13: 978-1-118-44333-0]

# Python PuLP solution prepared by Thomas W. Miller
# Revised April 20, 2023
# Implemented using activities dictionary with derived start_times and end_times
# rather than time decision variables as in Williams (2013)

from pulp import *

scenarios = {0: "Best Case Scenario", 1: "Expected Scenario", 2: "Worst Case Scenario"}


for scenario in range(0, 3):
    # Create a dictionary of the activities and their durations
    activities = {
        "DescribeProduct": [2, 4, 8],
        "DevelopMarketingStrategy": [4, 8, 16],
        "DesignBrochure": [4, 8, 16],
        "RequirementsAnalysis": [2, 4, 6],
        "SoftwareDesign": [4, 8, 16],
        "SystemDesign": [4, 8, 16],
        "Coding": [16, 40, 80],
        "WriteDocumentation": [8, 20, 40],
        "UnitTesting": [4, 12, 40],
        "SystemTesting": [4, 12, 40],
        "PackageDeliverables": [2, 4, 8],
        "SurveyPotentialMarket": [8, 20, 40],
        "DevelopPricingPlan": [2, 4, 16],
        "DevelopImplementationPlan": [8, 16, 24],
        "WriteClientProposal": [8, 16, 24],
    }

    # Create a list of the activities
    activities_list = list(activities.keys())

    # Create a dictionary of the activity precedences
    precedences = {
        "DescribeProduct": [],
        "DevelopMarketingStrategy": [],
        "DesignBrochure": ["DescribeProduct"],
        "RequirementsAnalysis": ["DescribeProduct"],
        "SoftwareDesign": ["RequirementsAnalysis"],
        "SystemDesign": ["RequirementsAnalysis"],
        "Coding": ["SoftwareDesign", "SystemDesign"],
        "WriteDocumentation": ["Coding"],
        "UnitTesting": ["Coding"],
        "SystemTesting": ["UnitTesting"],
        "PackageDeliverables": ["WriteDocumentation", "SystemTesting"],
        "SurveyPotentialMarket": ["DevelopMarketingStrategy", "DesignBrochure"],
        "DevelopPricingPlan": ["PackageDeliverables", "SurveyPotentialMarket"],
        "DevelopImplementationPlan": ["DescribeProduct", "PackageDeliverables"],
        "WriteClientProposal": ["DevelopPricingPlan", "DevelopImplementationPlan"],
    }

    # Create the LP problem
    prob = LpProblem("Critical Path", LpMinimize)

    # Create the LP variables
    start_times = {
        activity: LpVariable(f"start_{activity}", 0, None)
        for activity in activities_list
    }
    end_times = {
        activity: LpVariable(f"end_{activity}", 0, None) for activity in activities_list
    }

    # Add the constraints
    for activity in activities_list:
        prob += (
            end_times[activity]
            == start_times[activity] + activities[activity][scenario],
            f"{activity}_duration",
        )
        for predecessor in precedences[activity]:
            prob += (
                start_times[activity] >= end_times[predecessor],
                f"{activity}_predecessor_{predecessor}",
            )

    # Set the objective function
    prob += (
        lpSum([end_times[activity] for activity in activities_list]),
        "minimize_end_times",
    )

    # Solve the LP problem
    status = prob.solve()

    # Print the results
    print(f"Critical Path time for {scenarios[scenario]}:")
    for activity in activities_list:
        if value(start_times[activity]) == 0:
            print(f"{activity} starts at time 0")
        if value(end_times[activity]) == max(
            [value(end_times[activity]) for activity in activities_list]
        ):
            print(f"{activity} ends at {value(end_times[activity])} hours in duration")

    # Print solution
    print("\nSolution variable values:")
    for var in prob.variables():
        if var.name != "_dummy":
            print(var.name, "=", var.varValue)
