#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Call Center Object Oriented Design

This module implements a call center simulation with employees at different
levels: Respondent, Manager, and Director. Calls are routed to the first
available employee, escalating up the hierarchy if needed.

Source: https://github.com/donnemartin/system-design-primer
"""

from collections import deque
from enum import Enum


class Rank(Enum):
    RESPONDENT = 0
    MANAGER = 1
    DIRECTOR = 2


class Call:
    """Represents an incoming call to the call center."""

    def __init__(self, caller_id: str):
        self.caller_id = caller_id
        self.rank = Rank.RESPONDENT
        self.employee = None

    def set_employee(self, employee: 'Employee'):
        self.employee = employee

    def __repr__(self):
        return f'Call(caller_id={self.caller_id}, rank={self.rank})'


class Employee:
    """Base class representing a call center employee."""

    def __init__(self, employee_id: int, name: str, rank: Rank, call_center: 'CallCenter'):
        self.employee_id = employee_id
        self.name = name
        self.rank = rank
        self.call_center = call_center
        self.current_call = None

    def is_available(self) -> bool:
        return self.current_call is None

    def take_call(self, call: Call):
        """Assign a call to this employee."""
        if not self.is_available():
            raise Exception(f'{self.name} is already on a call.')
        call.set_employee(self)
        self.current_call = call
        print(f'{self.rank.name} {self.name} is handling call from {call.caller_id}')

    def complete_call(self):
        """Mark the current call as complete and check for queued calls."""
        if self.current_call is None:
            return
        print(f'{self.rank.name} {self.name} completed call from {self.current_call.caller_id}')
        self.current_call = None
        self.call_center.notify_available(self)

    def escalate_call(self):
        """Escalate the current call to a higher-ranked employee."""
        if self.current_call is None:
            return
        call = self.current_call
        self.current_call = None
        call.rank = Rank(self.rank.value + 1)
        self.call_center.dispatch_call(call)

    def __repr__(self):
        return f'{self.rank.name}({self.name})'


class Respondent(Employee):
    def __init__(self, employee_id, name, call_center):
        super().__init__(employee_id, name, Rank.RESPONDENT, call_center)


class Manager(Employee):
    def __init__(self, employee_id, name, call_center):
        super().__init__(employee_id, name, Rank.MANAGER, call_center)


class Director(Employee):
    def __init__(self, employee_id, name, call_center):
        super().__init__(employee_id, name, Rank.DIRECTOR, call_center)


class CallCenter:
    """Manages employees and dispatches incoming calls."""

    def __init__(self):
        self.employees = {
            Rank.RESPONDENT: [],
            Rank.MANAGER: [],
            Rank.DIRECTOR: [],
        }
        self.call_queue = {
            Rank.RESPONDENT: deque(),
            Rank.MANAGER: deque(),
            Rank.DIRECTOR: deque(),
        }

    def add_employee(self, employee: Employee):
        self.employees[employee.rank].append(employee)

    def dispatch_call(self, call: Call):
        """Dispatch a call to the first available employee at the required rank."""
        for rank in list(Rank)[call.rank.value:]:
            for employee in self.employees[rank]:
                if employee.is_available():
                    employee.take_call(call)
                    return
        # No one available — queue the call
        print(f'No available employee for {call}. Queuing call.')
        self.call_queue[call.rank].append(call)

    def notify_available(self, employee: Employee):
        """Called when an employee becomes available; assign queued calls if any."""
        queue = self.call_queue[employee.rank]
        if queue:
            call = queue.popleft()
            employee.take_call(call)


if __name__ == '__main__':
    center = CallCenter()

    r1 = Respondent(1, 'Alice', center)
    r2 = Respondent(2, 'Bob', center)
    m1 = Manager(3, 'Carol', center)
    d1 = Director(4, 'Dave', center)

    for emp in [r1, r2, m1, d1]:
        center.add_employee(emp)

    call1 = Call('customer_001')
    call2 = Call('customer_002')
    call3 = Call('customer_003')

    center.dispatch_call(call1)
    center.dispatch_call(call2)
    center.dispatch_call(call3)  # Should be queued

    r1.complete_call()  # Should pick up queued call3
