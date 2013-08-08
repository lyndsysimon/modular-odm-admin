<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
<script src="http://code.jquery.com/jquery.js"></script>
<script src="/static/js/bootstrap.min.js"></script>

<form name="edit" method="POST" action="">
    <legend>${schema_type}</legend>
    % for key, value in data.iteritems():
        % if key != primary_name:
            <div class="form-group"><label>${key}</label><br>
            % if type(value) is list and 'foreign' in value:
                <textarea class="field span12" name=${key}>${value['value']}</textarea></div>
            % elif key=='body':
                <textarea class="field span12" name=${key}>${value}</textarea></div>
            % else:
                <input type="text" value=${value} name=${key}></div>
            % endif
        % endif
    % endfor
    <button type="submit"> submit me </button>
</form>