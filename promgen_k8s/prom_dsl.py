
# Basic DSL
# def rc_entry(**kwargs):
#   return kwargs

# Intermediate DSL
def drop(**kwargs):
  kwargs['action'] = 'drop'
  return kwargs

def keep(**kwargs):
  kwargs['action'] = 'keep'
  return kwargs

def labelmap(**kwargs):
  kwargs['action'] = 'labelmap'
  return kwargs

def replace(**kwargs):
  # TODO: replace is the default action, drop it?
  kwargs['action'] = 'replace'
  return kwargs

# Advanced DSL
def set_value(label_name, value):
  # replace target with given value unconditionally
  return replace(replacement=value, target_label=label_name)

def copy_value(src_label_name, tgt_label_name):
  # replace target with source unconditionally
  return replace(source_labels=[src_label_name], target_label=tgt_label_name)

def remove_label(label_name):
  # set empty value
  return set_value(label_name, '')
