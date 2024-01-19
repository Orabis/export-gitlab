import {computed, createApp, onMounted, ref} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

createApp({
    delimiters: ['{$', '$}'],
    setup() {
        const issues = ref([])
        const labels = ref([])
        const selectedLabels = ref([]);
        const issuesStates = ref("opened");
        const ids = ref("")

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

        const onChange = (newValue) => {
            console.log(newValue.target)
            issuesStates.value = newValue.target.value
        }

        const issuesFiltered = computed(() => {
            if (selectedLabels.value.length === 0) {
                return issues.value.filter((issue) => {
                    return issuesStates.value === issue.states;
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
        }
    },
}).mount('#app')
