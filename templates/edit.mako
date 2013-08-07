<h3>${type}</h3>
<form name="edit" method="POST" action="">
    % for key, value in data.iteritems():
        % if key != '_id':
            ${key}<br>
            <textarea name=${key}>${value}</textarea><br>
        % endif
    % endfor
    <button type="submit"> submit me </button>
</form>