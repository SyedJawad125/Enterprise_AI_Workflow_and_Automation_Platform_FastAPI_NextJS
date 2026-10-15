# # start.py
# from app.main import app
# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run(
#         "app.main:app",
#         host="127.0.0.1",  # Explicitly use localhost
#         port=8000,
#         reload=True,
#         log_level="debug"  # Get more detailed logs
#     )





"""
start.py
─────────
Script to start individual services in development mode.

For production, use: docker compose up

Usage:
    python start.py              # start API Gateway (main entry point)
    python start.py auth        # start auth-service
    python start.py workflow    # start workflow-service
    python start.py ai          # start ai-service
    python start.py integration # start integration-service
    python start.py notification # start notification-service
    python start.py audit       # start audit-service
    python start.py --port 9000 # custom port for gateway
"""
import subprocess
import sys
import argparse


SERVICES = {
    'gateway': {
        'module': 'app.main:app',
        'port': 8000,
        'name': 'API Gateway',
        'cwd': 'services/api-gateway',
    },
    'auth': {
        'module': 'app.main:app',
        'port': 8001,
        'name': 'Auth Service',
        'cwd': 'services/auth-service',
    },
    'workflow': {
        'module': 'app.main:app',
        'port': 8002,
        'name': 'Workflow Service',
        'cwd': 'services/workflow-service',
    },
    'ai': {
        'module': 'app.main:app',
        'port': 8003,
        'name': 'AI Service',
        'cwd': 'services/ai-service',
    },
    'integration': {
        'module': 'app.main:app',
        'port': 8004,
        'name': 'Integration Service',
        'cwd': 'services/integration-service',
    },
    'notification': {
        'module': 'app.main:app',
        'port': 8005,
        'name': 'Notification Service',
        'cwd': 'services/notification-service',
    },
    'audit': {
        'module': 'app.main:app',
        'port': 8006,
        'name': 'Audit Service',
        'cwd': 'services/audit-service',
    },
}


def main():
    import os
    parser = argparse.ArgumentParser(description='Start Enterprise AI Platform Services')
    parser.add_argument('service', nargs='?', default='gateway', choices=list(SERVICES.keys()),
                       help='Service to start (default: gateway)')
    parser.add_argument('--port', type=int, help='Override default port')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind')
    parser.add_argument('--prod', action='store_true', help='Production mode (no reload)')
    parser.add_argument('--workers', type=int, default=1, help='Number of workers (prod only)')
    args = parser.parse_args()

    service = SERVICES[args.service]
    port = args.port or service['port']
    cwd = service.get('cwd', '.')

    # Add parent directory to PYTHONPATH for shared modules
    env = os.environ.copy()
    parent_dir = os.path.abspath(os.path.join(cwd, '..'))
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = parent_dir + os.pathsep + env['PYTHONPATH']
    else:
        env['PYTHONPATH'] = parent_dir

    cmd = [
        'uvicorn', service['module'],
        '--host', args.host,
        '--port', str(port),
        '--log-level', 'info',
        '--reload-dir', os.path.abspath(cwd),
    ]

    if args.prod:
        cmd += ['--workers', str(args.workers)]
        print(f'🚀 Starting PRODUCTION {service["name"]} on {args.host}:{port} ({args.workers} workers)')
    else:
        cmd += ['--reload']
        print(f'🔧 Starting DEVELOPMENT {service["name"]} on {args.host}:{port} (auto-reload on)')

    print(f'   API Docs: http://localhost:{port}/api/docs\n')

    try:
        subprocess.run(cmd, cwd=cwd, env=env)
    except KeyboardInterrupt:
        print('\n👋 Server stopped.')


if __name__ == '__main__':
    main()

    