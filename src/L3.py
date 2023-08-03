import subprocess
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


# get agent wise ticket count
# get ticket repetiton count
# get department wise ticket transferd

node_script_path = "../helpers/csvTojson.js"
csvPath = "../assets/L3.csv"

# Execute the Node.js script
jsonResult = subprocess.run(
    ["node", node_script_path, csvPath], capture_output=True, text=True
)
jsonData = []

# Check the output and error
if jsonResult.returncode == 0:
    print("Node.js script executed successfully.")
    # print("Output:", jsonResult.stdout)
    try:
        jsonData = json.loads(jsonResult.stdout)
    except json.JSONDecodeError as err:
        print("error while parsing json", err)
else:
    print("Error executing Node.js script.")
    print("Error:", jsonResult.stderr)


# Agent wise ticket count
def agentTicketCount():
    agent_counts = {}
    for entry in jsonData:
        agent_name = entry["Agent Name"]
        if agent_name in agent_counts:
            agent_counts[agent_name] += 1
        else:
            agent_counts[agent_name] = 1

    # Extract agent names and counts
    agent_names = list(agent_counts.keys())
    entry_counts = list(agent_counts.values())

    # Visualize the data in a pie chart
    plt.pie(entry_counts, labels=agent_names, autopct="%d")
    plt.axis("equal")
    plt.title("Number of Tickets Assigned to Each Agent")
    plt.show()

    # def agentDepartmentTicketCount():
    # agent_department_counts = {}
    # agents = set()
    # departments = set()

    # for entry in jsonData:
    #     agent_name = entry["Agent Name"]
    #     department = entry["Transfred To"]
    #     agents.add(agent_name)
    #     departments.add(department)
    #     key = (agent_name, department)
    #     if key in agent_department_counts:
    #         agent_department_counts[key] += 1
    #     else:
    #         agent_department_counts[key] = 1

    # # Extract agent names and ticket counts for each department
    # agents = sorted(list(agents))
    # departments = sorted(list(departments))
    # ticket_counts = np.zeros((len(agents), len(departments)))

    # for i, agent in enumerate(agents):
    #     for j, department in enumerate(departments):
    #         ticket_counts[i][j] = agent_department_counts.get((agent, department), 0)

    # # Visualize the data in a grouped bar chart
    # num_agents = len(agents)
    # num_departments = len(departments)
    # department_colors = plt.cm.tab20.colors[:num_departments]

    # fig, ax = plt.subplots()
    # width = 0.8 / num_departments

    # for i in range(num_departments):
    #     bars = ax.bar(
    #         np.arange(len(agents)) + i * width,
    #         ticket_counts[:, i],
    #         width=width,
    #         label=departments[i],
    #         color=department_colors[i],
    #     )
    #     for bar in bars:
    #         height = bar.get_height()
    #         ax.annotate(
    #             "{}".format(int(height)),  # Convert height to integer for display
    #             xy=(bar.get_x() + bar.get_width() / 2, height),
    #             xytext=(0, 3),  # 3 points vertical offset
    #             textcoords="offset points",
    #             ha="center",
    #             va="bottom",
    #         )

    # ax.set_xlabel("Agent Name")
    # ax.set_ylabel("Number of Tickets")
    # ax.set_title("Number of Tickets Transferred by Agents to Different Departments")
    # ax.set_xticks(np.arange(len(agents)) + (width * num_departments) / 2)
    # ax.set_xticklabels(agents)
    # ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
    # plt.xticks(rotation=45, ha="right")
    # plt.tight_layout()
    # plt.show()


# agentDepartmentTicketCount
def agentDepartmentTicketCount():
    agent_department_counts = {}
    agents = set()
    departments = set()

    for entry in jsonData:
        agent_name = entry["Agent Name"]
        department = entry["Transfred To"]
        agents.add(agent_name)
        departments.add(department)
        key = (agent_name, department)
        if key in agent_department_counts:
            agent_department_counts[key] += 1
        else:
            agent_department_counts[key] = 1

    # Extract agent names and ticket counts for each department
    agents = sorted(list(agents))
    departments = sorted(list(departments))
    ticket_counts = np.zeros((len(agents), len(departments)))

    for i, agent in enumerate(agents):
        for j, department in enumerate(departments):
            ticket_counts[i][j] = agent_department_counts.get((agent, department), 0)

    # Visualize the data in a stacked bar chart
    num_agents = len(agents)
    num_departments = len(departments)
    department_colors = plt.cm.tab20.colors[:num_departments]

    fig, ax = plt.subplots()

    bottom = np.zeros(num_agents)  # Initialize the bottom position for each bar segment
    for i in range(num_departments):
        ax.bar(
            np.arange(len(agents)),
            ticket_counts[:, i],
            bottom=bottom,
            width=0.8,
            label=departments[i],
            color=department_colors[i],
        )
        bottom += ticket_counts[:, i]

    for i, agent in enumerate(agents):
        for j, department in enumerate(departments):
            count = ticket_counts[i][j]
            if count != 0:
                height = count
                ax.annotate(
                    "{}".format(int(height)),  # Convert height to integer for display
                    xy=(i, bottom[i] - count / 2),
                    xytext=(5, 0),  # 5 points horizontal offset
                    textcoords="offset points",
                    ha="left",
                    va="center",
                )

    ax.set_xlabel("Agent Name")
    ax.set_ylabel("Number of Tickets")
    ax.set_title("Number of Tickets Transferred by Agents to Different Departments")
    ax.set_xticks(np.arange(len(agents)))
    ax.set_xticklabels(agents)
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# agentDepartmentTicketCountUnique
def agentDepartmentTicketCountUnique():
    agent_department_tickets = (
        {}
    )  # Dictionary to store unique tickets transferred by each agent to each department
    agents = set()
    departments = set()

    for entry in jsonData:
        agent_name = entry["Agent Name"]
        department = entry["Transfred To"]
        ticket_number = entry["Ticket Number"]

        agents.add(agent_name)
        departments.add(department)
        key = (agent_name, department)

        if key not in agent_department_tickets:
            agent_department_tickets[key] = set()

        agent_department_tickets[key].add(ticket_number)

    # Extract agent names and ticket counts for each department
    agents = sorted(list(agents))
    departments = sorted(list(departments))
    ticket_counts = np.zeros((len(agents), len(departments)))

    for i, agent in enumerate(agents):
        for j, department in enumerate(departments):
            ticket_counts[i][j] = len(
                agent_department_tickets.get((agent, department), set())
            )

    # Visualize the data in a stacked bar chart
    num_agents = len(agents)
    num_departments = len(departments)
    department_colors = plt.cm.tab20.colors[:num_departments]

    fig, ax = plt.subplots()

    bottom = np.zeros(num_agents)  # Initialize the bottom position for each bar segment
    for i in range(num_departments):
        ax.bar(
            np.arange(len(agents)),
            ticket_counts[:, i],
            bottom=bottom,
            width=0.8,
            label=departments[i],
            color=department_colors[i],
        )
        bottom += ticket_counts[:, i]

    for i, agent in enumerate(agents):
        for j, department in enumerate(departments):
            count = ticket_counts[i][j]
            if count != 0:
                height = count
                ax.annotate(
                    "{}".format(int(height)),  # Convert height to integer for display
                    xy=(i, bottom[i] - count / 2),
                    xytext=(5, 0),  # 5 points horizontal offset
                    textcoords="offset points",
                    ha="left",
                    va="center",
                )

    ax.set_xlabel("Agent Name")
    ax.set_ylabel("Number of Unique Tickets")
    ax.set_title(
        "Number of Unique Tickets Transferred by Agents to Different Departments"
    )
    ax.set_xticks(np.arange(len(agents)))
    ax.set_xticklabels(agents)
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# transferedTicketType
def transferedTicketType():
    agents_ticket_types_count = (
        {}
    )  # Dictionary to store counts of ticket types for each agent

    for entry in jsonData:
        agent_name = entry["Agent Name"]
        ticket_type = entry["Ticket Type"]

        if agent_name not in agents_ticket_types_count:
            agents_ticket_types_count[agent_name] = {}

        if ticket_type in agents_ticket_types_count[agent_name]:
            agents_ticket_types_count[agent_name][ticket_type] += 1
        else:
            agents_ticket_types_count[agent_name][ticket_type] = 1

    # Create the stacked bar graph
    agents = list(agents_ticket_types_count.keys())  # List of agent names
    ticket_types = list(
        set(
            ticket_type
            for agent in agents_ticket_types_count.values()
            for ticket_type in agent.keys()
        )
    )  # List of unique ticket types

    # Initialize the ticket type counts for each agent
    ticket_type_counts = {
        agent: [
            agents_ticket_types_count[agent].get(ticket_type, 0)
            for ticket_type in ticket_types
        ]
        for agent in agents
    }

    # Create the stacked bar graph
    fig, ax = plt.subplots()
    width = 0.8

    bottom = [0] * len(agents)  # Initialize the bottom position for each bar segment
    for i, ticket_type in enumerate(ticket_types):
        counts = [agent_counts[i] for agent_counts in ticket_type_counts.values()]
        ax.bar(agents, counts, width=width, label=ticket_type, bottom=bottom)
        bottom = [b + c for b, c in zip(bottom, counts)]

        # Add labels on top of each bar segment
        for j, count in enumerate(counts):
            if count != 0:
                height = count
                ax.annotate(
                    "{}".format(int(height)),  # Convert height to integer for display
                    xy=(j, bottom[j] - count / 2),
                    xytext=(5, 0),  # 5 points horizontal offset
                    textcoords="offset points",
                    ha="left",
                    va="center",
                )

    ax.set_xlabel("Agent Name")
    ax.set_ylabel("Count")
    ax.set_title("Ticket Type Counts per Agent")
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def ticketRepitition():
    ticket_department_counts = {}

    for entry in jsonData:
        ticket_number = entry["Ticket Number"]
        department = entry["Transfred To"]

        if ticket_number not in ticket_department_counts:
            ticket_department_counts[ticket_number] = {}

        if department in ticket_department_counts[ticket_number]:
            ticket_department_counts[ticket_number][department] += 1
        else:
            ticket_department_counts[ticket_number][department] = 1

    # Create the stacked bar graph
    ticket_numbers = list(ticket_department_counts.keys())  # List of ticket numbers
    departments = list(
        set(
            department
            for ticket_data in ticket_department_counts.values()
            for department in ticket_data.keys()
        )
    )  # List of unique departments

    # Initialize the department counts for each ticket number
    department_counts = {
        ticket_number: [
            ticket_department_counts[ticket_number].get(department, 0)
            for department in departments
        ]
        for ticket_number in ticket_numbers
    }

    # Create the stacked bar graph
    fig, ax = plt.subplots()
    width = 0.8

    bottom = [0] * len(
        ticket_numbers
    )  # Initialize the bottom position for each bar segment
    for i, department in enumerate(departments):
        counts = [ticket_counts[i] for ticket_counts in department_counts.values()]
        ax.bar(ticket_numbers, counts, width=width, label=department, bottom=bottom)
        bottom = [b + c for b, c in zip(bottom, counts)]

        # Add labels on top of each bar segment
        for j, count in enumerate(counts):
            if count != 0:
                height = count
                ax.annotate(
                    "{}".format(int(height)),  # Convert height to integer for display
                    xy=(j, bottom[j] - count / 2),
                    xytext=(5, 0),  # 5 points horizontal offset
                    textcoords="offset points",
                    ha="left",
                    va="center",
                )

    ax.set_xlabel("Ticket Number")
    ax.set_ylabel("Count")
    ax.set_title("Ticket Number Counts per Department")
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


agentTicketCount()
agentDepartmentTicketCount()
agentDepartmentTicketCountUnique()
transferedTicketType()
ticketRepitition()
