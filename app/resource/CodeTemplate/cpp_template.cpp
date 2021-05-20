enum {{dict_state_info['StateName']}} {
{% for state in dict_state_info['StateList'] %}    {{state}},
{% endfor %}
};

class {{dict_class_info['ClassName']}} {
    {% for action, dict_point in dict_class_info['FuncInfo'].items() %}
    void {{action}}()
    {        
        assert({{dict_point['from']}});        
        // TODO

        state_ = {{dict_point['to']}};
    }
    {% endfor %}
 private:
    {{dict_state_info['StateName']}} state_;
};