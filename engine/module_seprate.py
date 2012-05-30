def module_seperate(ID2net):
    # L1 ID2net should be dict[ID] = {ID1:"",ID2:"",ID3:""...}
    _mod_groups = {}
    _node_viewed = []
    _stop_degree = 2
    while len(_node_viewed) < len(ID2net):
        _max_degree = 0
        _max_id = None
        for _ID in ID2net:
            if _ID in _node_viewed:
                continue
            _degree = len([n for n in ID2net[_ID] if n not in _node_viewed])
            if _degree > _max_degree:
                _max_degree = _degree
                _max_id = _ID

        if _max_degree < _stop_degree:
            break

        _mod_groups[_max_id] = [_max_id]
        _node_viewed.append(_max_id)

        _node_remove = []
        for _ID in ID2net[_max_id]:
            if _ID in _node_viewed:
                continue
            _degree = len([n for n in ID2net[_ID] if n in ID2net[_max_id] and n != _max_id])
            if _degree == 0:
                _node_remove.append(_ID)

        for _ID in ID2net[_max_id]:
            if _ID not in _node_viewed and _ID not in _node_remove:
                _node_viewed.append(_ID)
                _mod_groups[_max_id].append(_ID)
    return _mod_groups

