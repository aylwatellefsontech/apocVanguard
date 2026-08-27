import type { ReactNode } from 'react'
import {
  calculateOptionPoints,
  formatOptionBody,
  formatOptionLabel,
} from '../utils/formatOption'
import {
  formatChooseLimitHeading,
  formatExclusiveGroupLegend,
  formatPerModelsSlotLegend,
  getModelCount,
  getChooseDisplayInstanceCount,
  getChooseLimit,
  getOptionGroup,
  getPerModelsDisplaySlotCount,
  getPerModelsInterval,
  getChooseOneChoices,
  getUpToLimit,
  isChooseOneOption,
  isUpToOption,
  isExclusiveGroupOption,
  isOptionSelected,
  isPerModelOption,
  isPerModelsOption,
  optionSelectionKey,
} from '../utils/optionUtils'
import type { OptionToggleContext, SelectedOption, UnitOption, UnitStats } from '../types'

interface UnitOptionsProps {
  options?: UnitOption[]
  interactive?: boolean
  selectedOptionIndexes?: number[]
  selectedOptions?: SelectedOption[]
  profileStats?: UnitStats | null
  onToggleOption?: (optionIndex: number, option: UnitOption, context?: OptionToggleContext) => void
  showSelectHint?: boolean
  highlightSelection?: boolean
  hideUnselected?: boolean
}

function groupExclusiveOptions(optionIndices: number[], options: UnitOption[]) {
  const groups = new Map<string, number[]>()
  const standalone: number[] = []

  for (const index of optionIndices) {
    const option = options[index]
    const group = getOptionGroup(option)
    if (isExclusiveGroupOption(option) && group) {
      const key = group.toLowerCase()
      const list = groups.get(key) ?? []
      list.push(index)
      groups.set(key, list)
    } else {
      standalone.push(index)
    }
  }

  return { groups, standalone }
}

function OptionLine({
  option,
  index,
  points,
  interactive,
  highlightSelection,
  hideUnselected = false,
  isSelected,
  inputType,
  inputName,
  modelIndex,
  slotIndex,
  choiceIndex,
  displayText,
  onToggleOption,
}: {
  option: UnitOption
  index: number
  points: number
  interactive: boolean
  highlightSelection: boolean
  hideUnselected: boolean
  isSelected: boolean
  inputType: 'checkbox' | 'radio'
  inputName?: string
  modelIndex?: number
  slotIndex?: number
  choiceIndex?: number
  displayText?: string
  onToggleOption?: (optionIndex: number, option: UnitOption, context?: OptionToggleContext) => void
}) {
  if (hideUnselected && !interactive && !isSelected) {
    return null
  }

  const label = typeof option === 'string' ? 'Option' : formatOptionLabel(option)
  const body = typeof option === 'string' ? option : formatOptionBody(option)
  const caption = displayText ?? (
    <>
      {label ? (
        <>
          <strong>{label}:</strong> {body}
        </>
      ) : (
        body
      )}
    </>
  )
  const pointsBadge = points > 0 ? <span className="option-pts"> +{points} Pt</span> : null

  if (interactive) {
    const toggle = () =>
      onToggleOption?.(index, option, {
        modelIndex,
        slotIndex,
        choiceIndex,
      })

    return (
      <li className={isSelected ? 'option-item selected' : 'option-item'}>
        <label className="option-toggle">
          <input
            type={inputType}
            name={inputName}
            checked={isSelected}
            onClick={
              inputType === 'radio' && isSelected ? toggle : undefined
            }
            onChange={inputType === 'checkbox' || !isSelected ? toggle : undefined}
          />
          <span className="option-toggle-text">
            {caption}
            {pointsBadge}
          </span>
        </label>
      </li>
    )
  }

  if (highlightSelection) {
    return (
      <li className={`option-item${isSelected ? ' selected' : ' dimmed'}`}>
        {caption}
        {pointsBadge}
      </li>
    )
  }

  return (
    <li>
      {caption}
      {pointsBadge}
    </li>
  )
}

function renderUpToCheckboxSlots(
  index: number,
  option: UnitOption,
  limit: number,
  _options: UnitOption[],
  profileStats: UnitStats | null,
  interactive: boolean,
  highlightSelection: boolean,
  hideUnselected: boolean,
  selectedOptionIndexes: number[],
  selectedOptions: SelectedOption[] | undefined,
  modelIndex?: number,
  onToggleOption?: (optionIndex: number, option: UnitOption, context?: OptionToggleContext) => void,
) {
  const label = typeof option === 'string' ? 'Option' : formatOptionLabel(option)
  const points =
    typeof option === 'string' ? 0 : calculateOptionPoints(option, profileStats, 'perSelection')

  const lines = Array.from({ length: limit }, (_, slotIndex) => {
    const isSelected = isOptionSelected(
      index,
      selectedOptionIndexes,
      selectedOptions,
      modelIndex,
      slotIndex,
    )
    return (
      <OptionLine
        key={optionSelectionKey(index, modelIndex, slotIndex)}
        option={option}
        index={index}
        points={points}
        interactive={interactive}
        highlightSelection={highlightSelection}
        hideUnselected={hideUnselected}
        isSelected={isSelected}
        inputType="checkbox"
        modelIndex={modelIndex}
        slotIndex={slotIndex}
        onToggleOption={onToggleOption}
      />
    )
  }).filter(Boolean)

  if (lines.length === 0) {
    return null
  }

  return (
    <fieldset key={`up-to-${index}-${modelIndex ?? 'unit'}`} className="option-group">
      <legend>
        {label} (up to {limit})
      </legend>
      <ul className="options-list options-list-interactive">{lines}</ul>
    </fieldset>
  )
}

function renderOptionBlock(
  optionIndices: number[],
  options: UnitOption[],
  profileStats: UnitStats | null,
  interactive: boolean,
  highlightSelection: boolean,
  hideUnselected: boolean,
  selectedOptionIndexes: number[],
  selectedOptions: SelectedOption[] | undefined,
  modelIndex?: number,
  onToggleOption?: (optionIndex: number, option: UnitOption, context?: OptionToggleContext) => void,
) {
  const { groups, standalone } = groupExclusiveOptions(optionIndices, options)
  const blocks: ReactNode[] = []
  const viewOnly = !interactive

  for (const [groupName, indices] of groups.entries()) {
    const sample = options[indices[0]]
    const displayName = getOptionGroup(sample) ?? groupName
    const groupLegend = formatExclusiveGroupLegend(displayName, viewOnly)
    const upToLimit = getUpToLimit(sample)
    const perModelsSlotCount = isPerModelsOption(sample)
      ? getPerModelsDisplaySlotCount(sample, profileStats, viewOnly)
      : 0

    if (upToLimit != null) {
      for (let slotIndex = 0; slotIndex < upToLimit; slotIndex += 1) {
        const lines = indices
          .map((index) => {
            const option = options[index]
            const points =
              typeof option === 'string' ? 0 : calculateOptionPoints(option, profileStats, 'perSelection')
            const isSelected = isOptionSelected(
              index,
              selectedOptionIndexes,
              selectedOptions,
              modelIndex,
              slotIndex,
            )
            return (
              <OptionLine
                key={optionSelectionKey(index, modelIndex, slotIndex)}
                option={option}
                index={index}
                points={points}
                interactive={interactive}
                highlightSelection={highlightSelection}
                hideUnselected={hideUnselected}
                isSelected={isSelected}
                inputType="radio"
                modelIndex={modelIndex}
                slotIndex={slotIndex}
                onToggleOption={onToggleOption}
              />
            )
          })
          .filter(Boolean)

        if (lines.length === 0) {
          continue
        }

        blocks.push(
          <fieldset
            key={`${groupName}-slot-${slotIndex}-${modelIndex ?? 'unit'}`}
            className="option-group"
          >
            <legend>
              {groupLegend} — choice {slotIndex + 1}
            </legend>
            <ul className="options-list options-list-interactive">{lines}</ul>
          </fieldset>,
        )
      }
    } else if (perModelsSlotCount > 0) {
      const interval = getPerModelsInterval(sample)!
      for (let slotIndex = 0; slotIndex < perModelsSlotCount; slotIndex += 1) {
        const lines = indices
          .map((index) => {
            const option = options[index]
            const points =
              typeof option === 'string'
                ? 0
                : calculateOptionPoints(option, profileStats, 'perSelection')
            const isSelected = isOptionSelected(
              index,
              selectedOptionIndexes,
              selectedOptions,
              modelIndex,
              slotIndex,
            )
            return (
              <OptionLine
                key={optionSelectionKey(index, modelIndex, slotIndex)}
                option={option}
                index={index}
                points={points}
                interactive={interactive}
                highlightSelection={highlightSelection}
                hideUnselected={hideUnselected}
                isSelected={isSelected}
                inputType="radio"
                modelIndex={modelIndex}
                slotIndex={slotIndex}
                onToggleOption={onToggleOption}
              />
            )
          })
          .filter(Boolean)

        if (lines.length === 0) {
          continue
        }

        blocks.push(
          <fieldset
            key={`${groupName}-per-models-${slotIndex}-${modelIndex ?? 'unit'}`}
            className="option-group"
          >
            <legend>{formatPerModelsSlotLegend(slotIndex, interval, groupLegend, viewOnly)}</legend>
            <ul className="options-list options-list-interactive">{lines}</ul>
          </fieldset>,
        )
      }
    } else if (!isPerModelsOption(sample)) {
      const lines = indices
        .map((index) => {
          const option = options[index]
          const points =
            typeof option === 'string' ? 0 : calculateOptionPoints(option, profileStats, 'perSelection')
          const isSelected = isOptionSelected(
            index,
            selectedOptionIndexes,
            selectedOptions,
            modelIndex,
          )
          return (
            <OptionLine
              key={optionSelectionKey(index, modelIndex)}
              option={option}
              index={index}
              points={points}
              interactive={interactive}
              highlightSelection={highlightSelection}
              hideUnselected={hideUnselected}
              isSelected={isSelected}
              inputType="radio"
              modelIndex={modelIndex}
              onToggleOption={onToggleOption}
            />
          )
        })
        .filter(Boolean)

      if (lines.length > 0) {
        blocks.push(
          <fieldset key={`${groupName}-${modelIndex ?? 'unit'}`} className="option-group">
            <legend>{groupLegend}</legend>
            <ul className="options-list options-list-interactive">{lines}</ul>
          </fieldset>,
        )
      }
    }
  }

  if (standalone.length > 0) {
    const listItems: ReactNode[] = []

    for (const index of standalone) {
      const option = options[index]
      const upToLimit = getUpToLimit(option)
      const perModelsSlotCount = isPerModelsOption(option)
        ? getPerModelsDisplaySlotCount(option, profileStats, viewOnly)
        : 0

      if (isChooseOneOption(option)) {
        const choices = getChooseOneChoices(option)
        const chooseLimit = getChooseLimit(option) ?? 1
        const instanceCount = getChooseDisplayInstanceCount(option, profileStats, viewOnly)
        if (instanceCount <= 0) {
          continue
        }
        const slotted = isUpToOption(option) || isPerModelsOption(option)
        const interval = getPerModelsInterval(option)
        const intro =
          typeof option === 'string' ? option : option.text?.trim() || `Choose ${chooseLimit}`
        const optionLabel = typeof option === 'string' ? 'Option' : formatOptionLabel(option)
        const chooseOnePoints =
          typeof option === 'string' ? 0 : calculateOptionPoints(option, profileStats, 'perSelection')
        const heading = optionLabel ? `${optionLabel}: ${intro}` : intro

        for (let instanceIndex = 0; instanceIndex < instanceCount; instanceIndex += 1) {
          const instanceSlot = slotted ? instanceIndex : undefined
          const instanceLabel =
            isPerModelsOption(option) && interval != null
              ? formatPerModelsSlotLegend(instanceIndex, interval, undefined, viewOnly)
              : slotted
                ? `choice ${instanceIndex + 1}`
                : null
          const lines = choices
            .map((choice, choiceIndex) => {
              const isSelected = isOptionSelected(
                index,
                selectedOptionIndexes,
                selectedOptions,
                modelIndex,
                instanceSlot,
                choiceIndex,
              )
              return (
                <OptionLine
                  key={optionSelectionKey(index, modelIndex, instanceSlot, choiceIndex)}
                  option={option}
                  index={index}
                  points={0}
                  interactive={interactive}
                  highlightSelection={highlightSelection}
                  hideUnselected={hideUnselected}
                  isSelected={isSelected}
                  inputType={chooseLimit === 1 ? 'radio' : 'checkbox'}
                  inputName={
                    chooseLimit === 1
                      ? `choose-${index}-${modelIndex ?? 'unit'}-${instanceIndex}`
                      : undefined
                  }
                  modelIndex={modelIndex}
                  slotIndex={instanceSlot}
                  choiceIndex={choiceIndex}
                  displayText={choice}
                  onToggleOption={onToggleOption}
                />
              )
            })
            .filter(Boolean)

          if (lines.length === 0) {
            continue
          }

          blocks.push(
            <fieldset
              key={`choose-${index}-${modelIndex ?? 'unit'}-${instanceIndex}`}
              className="option-group"
            >
              <legend>
                {instanceLabel ? `${heading} (${instanceLabel})` : heading}
                {chooseOnePoints > 0 ? ` +${chooseOnePoints} Pt` : ''}
              </legend>
              <p className="option-choose-heading">{formatChooseLimitHeading(chooseLimit)}</p>
              <ul className={`options-list${interactive ? ' options-list-interactive' : ''}`}>
                {lines}
              </ul>
            </fieldset>,
          )
        }
        continue
      }

      if (upToLimit != null && !isExclusiveGroupOption(option)) {
        const upToBlock = renderUpToCheckboxSlots(
          index,
          option,
          upToLimit,
          options,
          profileStats,
          interactive,
          highlightSelection,
          hideUnselected,
          selectedOptionIndexes,
          selectedOptions,
          modelIndex,
          onToggleOption,
        )
        if (upToBlock) {
          blocks.push(upToBlock)
        }
        continue
      }

      if (perModelsSlotCount > 0 && !isExclusiveGroupOption(option)) {
        const perModelsBlock = renderUpToCheckboxSlots(
          index,
          option,
          perModelsSlotCount,
          options,
          profileStats,
          interactive,
          highlightSelection,
          hideUnselected,
          selectedOptionIndexes,
          selectedOptions,
          modelIndex,
          onToggleOption,
        )
        if (perModelsBlock) {
          blocks.push(perModelsBlock)
        }
        continue
      }

      const points =
        typeof option === 'string' ? 0 : calculateOptionPoints(option, profileStats, 'perSelection')
      const isSelected = isOptionSelected(
        index,
        selectedOptionIndexes,
        selectedOptions,
        modelIndex,
      )
      listItems.push(
        <OptionLine
          key={optionSelectionKey(index, modelIndex)}
          option={option}
          index={index}
          points={points}
          interactive={interactive}
          highlightSelection={highlightSelection}
          hideUnselected={hideUnselected}
          isSelected={isSelected}
          inputType="checkbox"
          modelIndex={modelIndex}
          onToggleOption={onToggleOption}
        />,
      )
    }

    const visibleListItems = listItems.filter(Boolean)
    if (visibleListItems.length > 0) {
      blocks.push(
        <ul
          key={`standalone-${modelIndex ?? 'unit'}`}
          className={`options-list${interactive ? ' options-list-interactive' : ''}`}
        >
          {visibleListItems}
        </ul>,
      )
    }
  }

  return blocks.filter(Boolean)
}

export default function UnitOptions({
  options,
  interactive = false,
  selectedOptionIndexes = [],
  selectedOptions,
  profileStats = null,
  onToggleOption,
  showSelectHint = false,
  highlightSelection = false,
  hideUnselected = false,
}: UnitOptionsProps) {
  if (!options?.length) {
    return null
  }

  if (
    hideUnselected &&
    (selectedOptions?.length ?? 0) === 0 &&
    selectedOptionIndexes.length === 0
  ) {
    return null
  }

  const modelCount = getModelCount(profileStats)
  const perModelIndices = options
    .map((option, index) => (isPerModelOption(option) ? index : -1))
    .filter((index) => index >= 0)
  const perModelsIndices = options
    .map((option, index) => (isPerModelsOption(option) ? index : -1))
    .filter((index) => index >= 0)
  const unitIndices = options
    .map((option, index) =>
      !isPerModelOption(option) && !isPerModelsOption(option) ? index : -1,
    )
    .filter((index) => index >= 0)

  const unitBlocks =
    unitIndices.length > 0
      ? renderOptionBlock(
          unitIndices,
          options,
          profileStats,
          interactive,
          highlightSelection,
          hideUnselected,
          selectedOptionIndexes,
          selectedOptions,
          undefined,
          onToggleOption,
        )
      : []
  const perModelsBlocks =
    perModelsIndices.length > 0
      ? renderOptionBlock(
          perModelsIndices,
          options,
          profileStats,
          interactive,
          highlightSelection,
          hideUnselected,
          selectedOptionIndexes,
          selectedOptions,
          undefined,
          onToggleOption,
        )
      : []

  return (
    <section>
      <h3>Options</h3>
      {showSelectHint && (
        <p className="options-help muted">
          Add a profile from this unit to your roster, then select it to choose options.
        </p>
      )}
      {interactive && (
        <p className="options-help muted">
          Toggle options for the selected roster entry. Power Rating costs are added to the unit
          total.
        </p>
      )}

      {unitBlocks}
      {perModelsBlocks}
      {perModelIndices.length > 0 &&
        Array.from({ length: modelCount }, (_, modelIndex) => {
          const modelBlocks = renderOptionBlock(
            perModelIndices,
            options,
            profileStats,
            interactive,
            highlightSelection,
            hideUnselected,
            selectedOptionIndexes,
            selectedOptions,
            modelIndex,
            onToggleOption,
          )
          if (modelBlocks.length === 0) {
            return null
          }
          return (
            <div key={`model-${modelIndex}`} className="option-model-block">
              <h4 className="option-model-heading">Model {modelIndex + 1}</h4>
              {modelBlocks}
            </div>
          )
        })}
    </section>
  )
}
