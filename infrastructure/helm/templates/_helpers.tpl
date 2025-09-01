{{- define "cloudmind-backend.name" -}}
cloudmind-backend
{{- end -}}

{{- define "cloudmind-backend.fullname" -}}
{{ printf "%s-%s" .Release.Name (include "cloudmind-backend.name" .) | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{- define "cloudmind-backend.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

