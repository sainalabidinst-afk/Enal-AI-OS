"""Fix remaining mypy errors."""
import ast


def fix_mikrotik():
    with open('apps/network_engineer/vendor/mikrotik.py', 'r') as f:
        content = f.read()

    # Fix: broken NAT rules - extra parens + never appended
    target_start = '        # NAT Rules'
    target_end = '        # DHCP Servers'

    idx_start = content.find(target_start)
    idx_end = content.find(target_end)

    if idx_start < 0 or idx_end < 0:
        print('mikrotik.py: Could not find NAT/DHCP markers')
        return False

    old_block = content[idx_start:idx_end]
    new_block = (
        '        # NAT Rules\n'
        '        for nat_rule in config.nat_rules:\n'
        '            nat_action = self._map_nat_action(nat_rule.action)\n'
        '            ast.nat_rules.append(UniversalNATRule(\n'
        '                id=f"nat-{len(ast.nat_rules)}",\n'
        '                chain=nat_rule.chain,\n'
        '                action=nat_action,\n'
        '                src_address=nat_rule.src_address,\n'
        '                dst_address=nat_rule.dst_address,\n'
        '                in_interface=nat_rule.in_interface,\n'
        '                out_interface=nat_rule.out_interface,\n'
        '                comment=nat_rule.comment,\n'
        '            ))\n'
        '\n'
        '        # DHCP Servers\n'
    )

    content = content.replace(old_block, new_block)

    try:
        ast.parse(content)
        with open('apps/network_engineer/vendor/mikrotik.py', 'w') as f:
            f.write(content)
        print('mikrotik.py: Fixed syntax + added missing append')
        return True
    except SyntaxError as e:
        print(f'mikrotik.py: Syntax error after fix - {e}')
        return False


def fix_task_queue():
    with open('backend/app/core/task_queue.py', 'r') as f:
        content = f.read()

    # Fix: register_handler missing return type
    old = '    def register_handler(self, agent: str, handler: Callable[[Task], Awaitable[None]]):'
    new = '    def register_handler(self, agent: str, handler: Callable[[Task], Awaitable[None]]) -> None:'

    if old in content:
        content = content.replace(old, new)
        try:
            ast.parse(content)
            with open('backend/app/core/task_queue.py', 'w') as f:
                f.write(content)
            print('task_queue.py: Fixed register_handler return type')
            return True
        except SyntaxError as e:
            print(f'task_queue.py: Syntax error - {e}')
            return False
    else:
        print('task_queue.py: Pattern not found')
        return False


def fix_society():
    with open('apps/society/society.py', 'r') as f:
        content = f.read()

    # Fix: remove SubtaskResult from import if present
    old_import = 'from apps.organization.task_planner import SubTask, SubtaskResult, TaskPlan, task_planner'
    new_import = 'from apps.organization.task_planner import SubTask, TaskPlan, task_planner'

    if old_import in content:
        content = content.replace(old_import, new_import)
        print('society.py: Removed SubtaskResult from import')

    # Fix: remove redundant type annotation on redefinition
    old_assign = '            results: list[dict[str, Any]] = []'
    new_assign = '            results = []'

    if old_assign in content:
        content = content.replace(old_assign, new_assign)
        print('society.py: Removed redundant annotation on redefinition')

    try:
        ast.parse(content)
        with open('apps/society/society.py', 'w') as f:
            f.write(content)
        print('society.py: Fixed')
        return True
    except SyntaxError as e:
        print(f'society.py: Syntax error - {e}')
        return False


def fix_ai_studio():
    with open('backend/app/studio/ai_studio.py', 'r') as f:
        content = f.read()

    # Fix: get_trace returning list|dict but declared as dict
    # Observability.get_trace returns dict|None, but the method says -> dict
    # The issue is it returns observability.get_trace() which is dict|list|None
    old = '        result = observability.get_trace(trace_id)'
    new = '        result: dict | None = observability.get_trace(trace_id)'

    if old in content:
        content = content.replace(old, new)
        try:
            ast.parse(content)
            with open('backend/app/studio/ai_studio.py', 'w') as f:
                f.write(content)
            print('ai_studio.py: Fixed type annotation')
            return True
        except SyntaxError as e:
            print(f'ai_studio.py: Syntax error - {e}')
            return False
    else:
        print('ai_studio.py: Pattern not found')
        return False


if __name__ == '__main__':
    results = []
    results.append(('mikrotik.py', fix_mikrotik()))
    results.append(('task_queue.py', fix_task_queue()))
    results.append(('society.py', fix_society()))
    results.append(('ai_studio.py', fix_ai_studio()))

    print('\n=== Results ===')
    for name, ok in results:
        status = 'OK' if ok else 'FAIL'
        print(f'  {name}: {status}')
