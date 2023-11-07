

@bp.route('/add_indicator', methods=('POST', 'GET'))

def add_indicator():
    if request.method == 'POST':
        indicator = {'kind': 'ao', 'fast': 'int',
                     'slow': 'int', 'offset': 'int'}
        indicator = jsonify(indicator)
        print(indicator)
        return indicator
