import {computed, createApp, onMounted, ref, watch} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

createApp({
    delimiters: ['{$', '$}'],
    setup() {
        const issues = ref([])
        const labels = ref([])
        const selectedLabels = ref([])
        const issuesStates = ref("opened")
        const ids = ref("")
        const filteredIds = ref([])
        const visibleIssueCount = ref(20)

        onMounted(async () => {
            const url = window.location.href;
            const result = /\/projects\/(?<id>\d+)\/selection\/$/.exec(url)
            const id = parseInt(result?.[1] ?? '-1')

            const labelsResponse = await fetch(`/projects/${id}/labels/`)
            labels.value = await labelsResponse.json()
            const issuesResponse = await fetch(`/projects/${id}/issues/`)
            issues.value = await issuesResponse.json()
            issues.value = issues.value.map(issue => ({...issue, checked: false}))
        })

        watch(ids, async () => {
            const matches = ids.value.match(/\d+/g);
            if (matches) {
                filteredIds.value = matches.map(Number);
            } else {
                filteredIds.value = []
            }

        })
        const onChange = (newValue) => {
            console.log(newValue.target)
            issuesStates.value = newValue.target.value
        }

        const showMoreIssues = () => {
            visibleIssueCount.value += 10
        }
        const visibleIssues = computed(() => issuesFiltered.value.slice(0, visibleIssueCount.value))
        const allIssuesDisplayed = computed(() => visibleIssueCount.value >= issuesFiltered.value.length)
        const issuesFiltered = computed(() => {

            if (filteredIds.value.length === 0 && selectedLabels.value.length === 0) {
                return issues.value.filter((issue) => {
                    return issuesStates.value === issue.states
                })
            }

            if (filteredIds.value.length >= 1) {
                return issues.value.filter((issue) => {
                    return filteredIds.value.includes(issue.iid)
                })
            }
            return issues.value.filter((issue) => {
                return issue.labels.some((label) => {
                    return selectedLabels.value.includes(label)
                }) && issuesStates.value === issue.states;
            })
        })


        const getColors = (labelName) => {
            const label = labels.value.find((label) => label.name === labelName)

            return {
                bgColor: label.bg_color,
                textColor: label.text_color,
            }
        }

        const nbChecked = computed(() => issues.value.reduce((acc, issue) => {
            if (issue.checked) return acc + 1
            return acc
        }, 0))
        const allChecked = computed(() => {
            if (issues.value.length === 0) return false

            return issues.value.every((issue) => issue.checked)
        })
        const toggleAllCheckboxes = () => {
            const isChecked = !allChecked.value;
            issues.value.forEach((issue) => {
                issue.checked = isChecked;
            });
        };
        return {
            labels,
            issues,
            getColors,
            nbChecked,
            allChecked,
            toggleAllCheckboxes,
            selectedLabels,
            issuesFiltered,
            issuesStates,
            onChange,
            ids,
            filteredIds,
            showMoreIssues,
            visibleIssues,
            allIssuesDisplayed,
        }
    },
}).mount('#app')
