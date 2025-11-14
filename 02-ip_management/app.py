"""
IP Management System - Flask Web Application
Enterprise Network Automation Suite

Author: Philipp Prinzen
Project: IHK Fachinformatiker Abschlussprojekt
Date: 2025-11-13

Flask web interface for IP management system.
Provides REST API and web UI for device inventory management.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from ip_manager import IPManager
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

# Initialize IP Manager
manager = IPManager("data/devices.yaml")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# WEB ROUTES (HTML Pages)
# ============================================================================

@app.route('/')
def index():
    """Dashboard - Main overview page"""
    try:
        # Get statistics for both sites
        hq_stats = manager.get_network_statistics('hq')
        branch_stats = manager.get_network_statistics('branch')
        total_stats = manager.get_network_statistics()

        # Get all sites
        sites = manager.get_all_sites()

        return render_template('dashboard.html',
                             hq_stats=hq_stats,
                             branch_stats=branch_stats,
                             total_stats=total_stats,
                             sites=sites)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/devices')
def devices_page():
    """Device list page with filters"""
    try:
        # Get filter parameters
        site = request.args.get('site', 'all')
        vlan = request.args.get('vlan', 'all')
        device_type = request.args.get('type', 'all')

        # Get devices based on filters
        if site == 'all':
            device_list = manager.get_all_devices()
        else:
            device_list = manager.get_all_devices(site)

        # Apply VLAN filter
        if vlan != 'all':
            device_list = [d for d in device_list if d.get('vlan') == int(vlan)]

        # Apply type filter
        if device_type != 'all':
            device_list = [d for d in device_list if d.get('type') == device_type]

        # Get unique values for filters
        sites = manager.get_all_sites()
        all_devices = manager.get_all_devices()
        vlans = sorted(set(d.get('vlan') for d in all_devices if d.get('vlan')))
        types = sorted(set(d.get('type') for d in all_devices if d.get('type')))

        return render_template('devices.html',
                             devices=device_list,
                             sites=sites,
                             vlans=vlans,
                             types=types,
                             current_site=site,
                             current_vlan=vlan,
                             current_type=device_type)
    except Exception as e:
        logger.error(f"Error loading devices: {e}")
        return render_template('error.html', error=str(e)), 500


@app.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    """Add new device form"""
    if request.method == 'POST':
        try:
            # Get form data
            site = request.form.get('site')
            device_data = {
                'name': request.form.get('name'),
                'type': request.form.get('type'),
                'vlan': int(request.form.get('vlan')),
                'ip': request.form.get('ip'),
                'port': request.form.get('port'),
                'switch': request.form.get('switch'),
                'status': request.form.get('status'),
                'description': request.form.get('description', '')
            }

            # Add optional role if server
            if device_data['type'] == 'server':
                role = request.form.get('role')
                if role:
                    device_data['role'] = role

            # Add device
            success = manager.add_device(site, device_data)

            if success:
                logger.info(f"Device {device_data['name']} added successfully")
                return redirect(url_for('devices_page'))
            else:
                return render_template('add_device.html',
                                     sites=manager.get_all_sites(),
                                     error="Failed to add device")
        except Exception as e:
            logger.error(f"Error adding device: {e}")
            return render_template('add_device.html',
                                 sites=manager.get_all_sites(),
                                 error=str(e))

    # GET request - show form
    sites = manager.get_all_sites()
    return render_template('add_device.html', sites=sites)


@app.route('/free-ips')
def free_ips_page():
    """Free IP address finder"""
    try:
        site = request.args.get('site', 'hq')
        vlan = request.args.get('vlan', '20')

        free_ip_list = []
        vlan_info = None

        if vlan and vlan != 'select':
            vlan_id = int(vlan)
            free_ip_list = manager.calculate_free_ips(vlan_id, site)
            vlan_info = manager.get_vlan_info(vlan_id, site)

        # Get site info for VLAN dropdown
        site_info = manager.get_site_info(site)
        sites = manager.get_all_sites()

        return render_template('free_ips.html',
                             sites=sites,
                             current_site=site,
                             vlans=site_info['vlans'],
                             current_vlan=vlan,
                             free_ips=free_ip_list,
                             vlan_info=vlan_info)
    except Exception as e:
        logger.error(f"Error calculating free IPs: {e}")
        return render_template('error.html', error=str(e)), 500


# ============================================================================
# REST API ENDPOINTS (JSON Responses)
# ============================================================================

@app.route('/api/sites')
def api_sites():
    """Get all sites"""
    try:
        sites = manager.get_all_sites()
        return jsonify({'sites': sites})
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices')
def api_devices():
    """Get all devices or filtered by site"""
    try:
        site = request.args.get('site')
        devices = manager.get_all_devices(site)
        return jsonify({'devices': devices, 'count': len(devices)})
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices/<site>/<device_name>')
def api_device_detail(site, device_name):
    """Get specific device details"""
    try:
        device = manager.get_device_by_name(device_name, site)
        if device:
            return jsonify({'device': device})
        else:
            return jsonify({'error': 'Device not found'}), 404
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def api_statistics():
    """Get network statistics"""
    try:
        site = request.args.get('site')
        stats = manager.get_network_statistics(site)
        return jsonify({'statistics': stats})
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/free-ips/<site>/<int:vlan_id>')
def api_free_ips(site, vlan_id):
    """Get free IP addresses for a VLAN"""
    try:
        free_ips = manager.calculate_free_ips(vlan_id, site)
        vlan_info = manager.get_vlan_info(vlan_id, site)
        return jsonify({
            'vlan': vlan_id,
            'site': site,
            'vlan_info': vlan_info,
            'free_ips': free_ips,
            'count': len(free_ips)
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices/add', methods=['POST'])
def api_add_device():
    """Add new device via API"""
    try:
        data = request.get_json()
        site = data.get('site')
        device_data = data.get('device')

        if not site or not device_data:
            return jsonify({'error': 'Missing site or device data'}), 400

        success = manager.add_device(site, device_data)

        if success:
            return jsonify({'success': True, 'message': 'Device added'})
        else:
            return jsonify({'error': 'Failed to add device'}), 500

    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices/update/<site>/<device_name>', methods=['PUT'])
def api_update_device(site, device_name):
    """Update device via API"""
    try:
        data = request.get_json()
        success = manager.update_device(site, device_name, data)

        if success:
            return jsonify({'success': True, 'message': 'Device updated'})
        else:
            return jsonify({'error': 'Failed to update device'}), 500

    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices/delete/<site>/<device_name>', methods=['DELETE'])
def api_delete_device(site, device_name):
    """Delete device via API"""
    try:
        success = manager.delete_device(site, device_name)

        if success:
            return jsonify({'success': True, 'message': 'Device deleted'})
        else:
            return jsonify({'error': 'Failed to delete device'}), 500

    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/csv')
def api_export_csv():
    """Export devices to CSV"""
    try:
        site = request.args.get('site')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'devices_{site if site else "all"}_{timestamp}.csv'

        manager.export_to_csv(filename, site)

        return jsonify({
            'success': True,
            'filename': filename,
            'message': f'Exported to {filename}'
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(_error):
    """404 error handler"""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(_error):
    """500 error handler"""
    return render_template('error.html', error='Internal server error'), 500


# ============================================================================
# TEMPLATE FILTERS
# ============================================================================

@app.template_filter('format_datetime')
def format_datetime(value):
    """Format datetime for templates"""
    if isinstance(value, str):
        return value
    return value.strftime('%Y-%m-%d %H:%M:%S')


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("Starting IP Management System Web Interface")
    logger.info("Access dashboard at: http://127.0.0.1:5000")

    # Run Flask development server
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True  # Set to False in production!
    )