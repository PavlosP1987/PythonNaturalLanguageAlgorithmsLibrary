import base64
import zlib
compressed = 'eJwdktkNgDAMQxfqR+5j/8V4QUJQUttx3Nrzl0+f+uunPPpm+Tf3Z/tKX1DM5bXP+wUFA777bCob4HMRfUk14QwfDYPrrA5gcuQB49lQQxdZpdr+1oN2bEA3pW5Nf8NGOFsR19NBszyX7G2raQpkVUEBdbTLuwSRlcDCYiW7GeBaRYJrgImrM3lmI/WsIxFXNd+aszXoRXuZ1PnZRdwKJeqYYYKq6y1++PXOYdgM0TlZcymCOdKqR7HYmYPiRslDr2Sn6C0Wgw+a6MakM2VnBk6HwU6uWqDRz+p6wtKTCg2WsfdKJwfJlHNaFT4+Q7PGfR9hyWK3p3464nhFwpOd7kdvjmz1jpWcxmbG/FJUXdMZgrpzs+jxC11twrBo3TaNgvsf8oqIYwT4r9XkPnNC1XcP7qD5cW7UHSJZ3my5qba+ozncl5kz8gGEEYOQ'
data = zlib.decompress(base64.b64decode(compressed))