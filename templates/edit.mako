<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
<link href="/static/css/bootstrap-glyphicons.css" rel="stylesheet" media="screen">
<script src="http://code.jquery.com/jquery.js"></script>
<script src="/static/js/bootstrap.min.js"></script>
<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>

<form name="edit" method="POST" action="" id="edit">
    <legend>${schema_name}</legend>
    % for key, value in schema_obj_data.iteritems():
        % if key!='_backrefs':
            <h4 style="margin-left: 5px;">${key}</h4><div class="form-group row" style="margin-left: 25px;">
        % endif
        % if key==schema_primary_name:
                            <ul class="list-group col-lg-4" id="${key}">
                    <li class="list-group-item form-control data" id="${key}" item="item" contenteditable>${value}</li>
                </ul></div>
        % elif type(value) is dict and 'foreign' in value:
                <ul class="list-group col-lg-4 ForeignField" id="${key}">
                <div style="position: relative;">
                    <li class="list-group-item form-control data" id="${key}" item="item" ondblclick="areYouSure(this)">${value['primary_value']}</li>
                <a href="/${value['schema_name']}/${value['primary_value']}/edit" style="position:absolute; top:9; right:9;" class="badge" data-toggle="popover" id="${value['primary_value']}" object-vals='${value['foreign_obj']}'><span class="glyphicon glyphicon-search"></span></a></div>
                </ul>
            </div>
        % elif type(value) is list:
            % if type(value[0]) is dict and 'foreign' in value[0]:
                <ul class="list-group col-lg-4 ForeignListField sortable" keyName="${key}">
                    % for item in value:
                    <div style="position:relative;" >
                        <li class="list-group-item form-control" item="item" onclick="areYouSure(this)" contenteditable>${item['primary_value']}</li>
                        <a class="badge glyphicon glyphicon-remove" style="position:absolute; top:9; right:38;" onclick="removeListItem(this)"> </a>
                        <a href="/${item['schema_name']}/${item['primary_value']}/edit" style="position:absolute; top:9; right:9;" class="badge" data-toggle="popover" id="${item['primary_value']}" object-vals='${item['foreign_obj']}'>
                            <span class="glyphicon glyphicon-search"></span></a><span class="handle glyphicon glyphicon-move" style="position:absolute; top:9; left:-15;"></span>
                    </div>
                    % endfor
                    <div class="placeholder" style="position: relative;"><li class="placeholder list-group-item form-control" id="${key}placeholder" onclick="$(this).text('');" onkeydown="addListItem($(this).text(), this)" contenteditable>add new...</li>
                    <a class="badge glyphicon glyphicon-plus" style="position:absolute; top:9; right:9;" onclick="addListItem($(this.parentNode).text(), this);"> </a>
                    </div>
                </ul>
                    <input type="text" id="${key}" style="display: none;" class="dataList">
                    </div>
            % else:
                <ul class="list-group ListField col-lg-4 sortable test1" keyName="${key}">
                    % for item in value:
                    <div style="position: relative;"><li item="item" class="list-group-item form-control" contenteditable>${item}</li>
                    <a class="badge glyphicon glyphicon-remove" style="position:absolute; top:9; right:9;" onclick="removeListItem(this)"> </a><span class="handle glyphicon glyphicon-move" style="position:absolute; top:9; left:-15;"></span>
                    </div>
                    % endfor
                    <input type="text" id="${key}" style="display: none;" value="${value}" class="dataList">
                    <div class="placeholder" style="position: relative;"><li class="placeholder list-group-item form-control" id="${key}placeholder" onclick="$(this).text('');" onkeydown="addListItem($(this).text(), this)" contenteditable>add new...</li>
                    <a class="badge glyphicon glyphicon-plus" style="position:absolute; top:9; right:9;" onclick="addListItem($(this.parentNode).text(), this);"> </a>
                    </div>
                </ul>
                    </div>
            %endif
        % elif key=='_backrefs':
            <h4 style="margin-left: 5px;">references</h4>
            % for refs, vals in value.iteritems():
                % for schema, schema_attr in vals.iteritems():
                    % for parent_field_name, parent_keys in schema_attr.iteritems():
                        <div class="row" style="margin-left: 25px;">
                        <ul class="list-group col-lg-4">
                        <h5>${refs}</h5>
                        % for parent_key in parent_keys:
                            <div style="position: relative;">
                                <li class="list-group-item form-control">${parent_key}</li>
                                <a href="/${schema}/${parent_key}/edit" style="position:absolute; top:9; right:9;" class="badge" data-toggle="popover" id="${parent_key}" object-vals='${parent_key}'>
                                <span class="glyphicon glyphicon-search"></span></a>
                            </div>
##                                <a class="badge glyphicon glyhref="/${schema}/${parent_key}/edit">${parent_key}</a>
                        % endfor
                        </ul>
                        </div>
                    % endfor
                % endfor
            % endfor
##                <textarea class="data col-lg-4" value="${value}">${value}</textarea></div>
        % elif key=='body' or type(value) is dict:
                <textarea class="data col-lg-4" value="${value}">${value}</textarea></div>
        % else:
                <ul class="list-group col-lg-4" id="${key}">
                    <li class="list-group-item form-control data" id="${key}" item="item" contenteditable>${value}</li>
                </ul></div>
        % endif
    % endfor
    <button type="submit"> submit me </button><P>${message}</P>
    <input type="text" id="submitter" style="display: none;" name="json_data">
</form>
<br>
<a href="/${schema_name}"><-${schema_name}</a>

<script>
    $(function(){
        $('.sortable').sortable({
            axis: 'y',
            containment: "parent",
            handle: $('.sortable').find('.handle'),
            items: "> div:not(.placeholder)",
            helper: "clone"
        });
        $('form').submit(function(){

            var search = $('.ListField');
            for(var i=0; i<search.length; i++){
                var hasher = "#" + $(search[i]).attr('keyName');
                var newList = $(search[i])
                        .find("[item='item']")
                        .map(function(){
                            return $(this).text()
                        })
                        .get();
                $(hasher).attr('value', newList);
            }

            var search = $('.ForeignListField');
            for(var i=0; i<search.length; i++){
                var hasher = "#" + $(search[i]).attr('keyName');
                var newList = $(search[i])
                        .find("[item='item']")
                        .map(function(){
                            return $(this).text()
                        })
                        .get();
                $(hasher).attr('value', newList);
            }



            var retval = {};
            $('.dataList').each(function(idx, elm){
                var key = $(elm).attr('id');
                var value = $(elm).attr('value');
                retval[key] = value;
            });

            $('.data').each(function(idx, elm){
                var key = $(elm).attr('id');
                var value = $(elm).text();
                retval[key] = value;
            });
            $("#submitter").attr('value', JSON.stringify(retval));

        });

        var search =$('.ForeignListField');
        for(var i=0; i<search.length; i++){
            $(search[i])
                    .find("[data-toggle='popover']")
                    .each(function(idx, elm) {
                        var id = $(elm).attr('id');
                        var item = JSON.parse($(elm).attr('object-vals'));
                        var hasher = "#" + id;
                        $(hasher).popover({
                            trigger: 'hover',
                            html: true,
                            content: popContent(item)
                        });
                    });
        }

        $('.ForeignField')
                .each(function(index, element){
                    $(element).find("[data-toggle='popover']")
                            .each(function(idx, elm){
                                var id = $(elm).attr('id');
                                var item = JSON.parse($(elm).attr('object-vals'));
                                var hasher = "#" + id;
                                $(hasher).popover({
                                    trigger: 'hover',
                                    html: true,
                                    content: popContent(item)
                                });
                            })
                });
    });

    $('#edit').keydown(function(e){
        if (e.keyCode==13){
            e.preventDefault();
            return true;
        }
    });

    function hidePops(show){
        $("[data-toggle='popover']").
                each(function(idx, elm){
                    if (elm!=show.parentElement){
                        $(elm).popover('hide');
                    }
                });
    }

    function findValue(elm){
        return $(elm).parent().find("[placeholder='add new...']" ).val();
    }

    function popContent(content){
        var keys=[];
        for (var key in content){
            if(content[key] instanceof Object){
                keys.push(key + ": " + JSON.stringify(content[key]) + "<br>");
            }
            else{
                keys.push(key + ": " + content[key] + "<br>");
            }
        }
        return keys;
    }

    function areYouSure(elm){
        var confirm_change = confirm("Are you sure you want to change this ForeignField?");
        if(confirm_change){
            $(elm).text('');
            $(elm.parentNode).find('a').remove();
            $(elm.parentNode).append("<a class='badge glyphicon glyphicon-plus' style='position:absolute; top:9; right:9;' onclick='checkExists(this)'> </a>")
        }
        else{
            $(elm).blur();
        }
    }

    function checkExists(elm){
        alert("Do something here with a post");
    }

    function removeListItem(elm){
        $(elm).parent().remove();
    }

    function addListItem(val, elm){
        if(event.keyCode==13){
##        var html = "<div style='position: relative;'><li class='list-group-item form-control' contenteditable>" + val + "<a class='badge glyphicon glyphicon-remove' style='position:absolute; top:9; right:9;' onclick='removeListItem(this)'> </a><span class='handle glyphicon glyphicon-move' style='position:absolute; top:9; left:-15;'></span></li></div>";
        var html = "<div style='position: relative;'><li item='item' class='list-group-item form-control' contenteditable>" + val + "</li><a class='badge glyphicon glyphicon-remove' style='position:absolute; top:9; right:9;' onclick='removeListItem(this)'> </a><span class='handle glyphicon glyphicon-move' style='position:absolute; top:9; left:-15;'></span></div>";
        var element = $(elm.parentNode);
        element.before(html);
        $(elm.parentNode).find('li').text('add new...');
        $(elm).blur();
        $(elm.parentNode.parentNode).sortable({
            handle: $('.sortable').find('.handle')
        });
        }
    }
</script>