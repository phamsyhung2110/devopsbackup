# Define Labels Template
{{- define "nginx-app.labels" }}
name: {{ .Release.Name }}
env: {{ .Values.env }}
{{- end -}}

# Define Resource Template
{{- define "nginx-app.resources" -}}
limits:
  memory: {{ .Values.resources.limits.memory }}
  cpu: {{ .Values.resources.limits.cpu }}
requests:
  memory: {{ .Values.resources.requests.memory }}
  cpu: {{ .Values.resources.requests.cpu }}
{{- end -}}

#Define Port Template
{{- define "nginx-app.port" -}}
port: {{ .port }}
targetPort: {{ .tgport }}
{{- end }}

